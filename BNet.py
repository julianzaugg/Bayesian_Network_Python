'''
Created on Dec 12, 2011

@author: julianzaugg
'''
#cython: profile=True

import itertools
import math

try:
    from cTable_Utils import entry
except ImportError, e:
    print e
    from Table_Utils import entry
from JPT import JPT


class BNet(object):
    """Defines a Bayesian network"""

    EM_CONV_CRIT = 0.00001
    EM_MAX_ITERS = 10000
    EM_DEBUG = False

    def __init__(self, nodes=None):
        if nodes is None:
            self.nodes = {}
        else:
            # Check that names are unique
            assert len({node.name for node in nodes}) == len(nodes)
            self.nodes = {node.name: node for node in nodes}
        self.trans_closures = {}

    def add(self, node):
        """Adds a node to the network"""
        if node.name in self.nodes:
            raise ValueError("Duplicate node name: " + node.name)
        #<insert GDT parent node check here later?>
        self.nodes[node.name] = node
        self.trans_closures = {}

    def get_roots(self):
        """Return all roots (i.e., nodes without parents) in the network"""
        return {node.name for node in self.nodes.values() if node.is_root()}

    def get_parents(self, nodename):
        """Return the parents of the node"""
        self.node_check([nodename])
        return self.nodes[nodename].labels

    def get_ancestors(self, nodename):
        """Returns the ancestors of the node"""
        # FIXME: Should be updated for get_relevant change
        self.node_check([nodename])
        new_nodes = set(self.get_parents(nodename))
        ancestors = set(new_nodes)
        while new_nodes:
            node = new_nodes.pop()
            ancestors.add(node)
            new_nodes |= set(self.nodes[node].labels) - ancestors
        return ancestors

    def get_children(self, nodename):
        """Return the immediate children of a node"""
        self.node_check([nodename])
        return {n.name for n in self.nodes.values() if nodename in n.labels}

    def get_leaves(self):
        """Return all leaves (i.e., nodes without children) in the network"""
        all_labels = [n.labels for n in self.nodes.values()]
        non_leaves = {i for i in itertools.chain(*all_labels)}
        return {node.name for node in self.nodes.values()} - non_leaves

    def get_topological_ordering(self):
        """
        Sorts and returns the network as a topological ordered list
        so that parent nodes are always referenced before child nodes
        """
        ordered = []
        leaves = self.get_leaves()
        visited = set()

        def visit(node):
            visited.add(node)
            for parent in self.nodes[node].labels:
                if parent not in visited:
                    visit(parent)
            ordered.append(node)

        for node in leaves:
            visit(node)
        return ordered

    # Suggest only use for debugging, call overhead is too large for
    # large scale networks
    def node_check(self, nodenames):
        """Determines if nodes with specified name are part of the network"""
        assert set(nodenames) <= set(self.nodes.keys()), \
            "Invalid node IDs: %s" % str(set(nodenames) - set(self.nodes.keys()))

    def connection_check(self):
        """
        Initiates a check to determine if the current
        specified network is valid
        i.e all nodes are connected to each each other
        """
        start_node = list(self.get_roots())[0]
        connected = self.df_connected(start_node, [])
        not_connected = [node for node in self.nodes.keys()
                         if node not in connected]
        assert len(connected) == len(self.nodes),\
        "There are unconnected nodes/node groups in this network : %s & %s" %\
        (connected, not_connected)

    def df_connected(self, nodename, visited):
        """
        Applies a depth-first search(?) from a specified node
        and returns a list of all (weakly and strongly) connected nodes.
        """
        if nodename not in visited:
            visited.append(nodename)
        connected_nodes = list(self.get_children(nodename)) + \
                                    self.get_parents(nodename)
        for cnode in connected_nodes:
            if cnode not in visited:
                visited.append(cnode)
                self.df_connected(cnode, visited)
        return visited

#    @profile
    def infer_naive(self, queries):
        """
        Initiates naive inference of a query variable.
        Returns a JPT of non-normalized values for
        a single query.
        infer_naive(list(node_names)) -> output(JPT)
        """
        self.node_check(queries)
        net = self.get_relevant(queries)
        variables = net.get_topological_ordering()
        observed_nodes = {}
        for name, node in net.nodes.iteritems():
            if node.instance is not None:
                observed_nodes[name] = node.instance
        jpt = JPT(queries)
        for i in range(jpt.maxrows):
            fill_vals = entry(i, len(jpt.labels))
            filled_observations = {k: v for k, v in zip(queries, fill_vals)}
            conflicted_values = False
            for k, v in filled_observations.iteritems():
                if k in observed_nodes and observed_nodes[k] != v:
                    conflicted_values = True
                    break
            if conflicted_values:
                jpt.put(fill_vals, 0.0)
                continue
            filled_observations.update(observed_nodes)
            variable_nodes = [net.nodes[v] for v in variables]
            inferred = net.enumerate_all(variable_nodes, filled_observations)
            jpt.put(fill_vals, inferred)
        return jpt

#    @profile
    def enumerate_all(self, variables, e):
        """
        Enumerates through a list of variables (nodes), calculates
        conditional probability values for each node and
        returns the joint probability of the nodes.
        enumarate_all(node_list, observed_node_list) ->
        output(value)
        """
        if not variables:
            return 1.0
        Y, rest = variables[0], variables[1:]
        #Since our network variables list is in topological order
        #parents nodes should have been already calculated prior
        #the current child node.
        pinstances = [e[p] for p in Y.labels]
        if Y.name in e:
            return Y.get(e[Y.name], pinstances) * self.enumerate_all(rest, e)
        else:
            temp = 0
            for instance in [True, False]:
                recursive_observations = dict(e)
                recursive_observations[Y.name] = instance
                temp += (Y.get(instance, pinstances) *
                         self.enumerate_all(rest, recursive_observations))
            return temp

    def get_relevant(self, query):
        """Return a BNet with a minimal node set for the query and evidence"""

        # This is an optimisation to avoid expensive recalculation of
        # ancestors (i.e., transitive closures).
        if not self.trans_closures:
            closures = {}
            for name, node in self.nodes.iteritems():
                closure = set()
                parents = set(node.labels)
                while parents:
                    node = self.nodes[parents.pop()]
                    closure.add(node.name)
                    parents |= set(node.labels) - closure
                closures[name] = {self.nodes[n] for n in closure}
            self.trans_closures = closures

        # Query nodes and all instantiated nodes are relevant
        relevant = {n for n in self.nodes.values()
                    if n.instance is not None or n.name in query}
        # Looks magic; just getting the set of all closures of relevant nodes
        closure = set.union(*(self.trans_closures[n.name] for n in relevant))
        return BNet(relevant | closure)

    def train_list(self, labels, hid_labels):
        """
        Here we create the list of nodes that will be updated during
        training, note that only nodes that are named as observed or hidden
        variables will be included
        """
        updatenames = {a for a in labels + hid_labels}
        update = set()
        for node in self.nodes.values():
            if node.name in updatenames:
                parentsallthere = True
                parents = self.get_parents(node.name)
                for p in parents:
                    if p not in updatenames:
                        parentsallthere = False
                if parentsallthere:
                    update.add(node)
        return update

    def node_randomize(self, labels, sort_values, values, seed):
        """
        Randomize nodes that will be updated as part of learning
        Values for nodes first assigned here!
        """
        sort_values.sort()
        cnt = 0
        for s in sort_values:
            node = self.nodes[s]
            if node.trainable:
                observed = -1
                for i in labels:
                    if i == node.name:
                        observed = labels.index(i)
                        break
                if observed > -1:
                    observations = [values[j][observed] for j in
                                    range(len(values))]
                    #this allows a node to peek what data is going to be
                    #presented later (useful to find good initial setting)
                    cnt += 1
                    node.randomize(seed + cnt, observations)
                else:
                    #Hidden nodes go here
                    cnt += 1
                    node.randomize(seed + cnt, [])

    def train(self, labels, values, hid_labels=None, seed=1):
        """
        Train the BN using expectation maximization
        """

        if hid_labels is None:
            hid_labels = []

        # Set up the network state
        update = self.train_list(labels, hid_labels)
        self.node_randomize(labels, [nn.name for nn in update], values, seed)

        # Initialize learning parameters
        log_prob = -999998.0
        prev_prob = 999999.0
        conv_rate = 0.02
        roundn = 0
        latent_variable_exist = False

        # Train until convergence occurs or max rounds is reached
        while conv_rate > self.EM_CONV_CRIT and roundn < self.EM_MAX_ITERS:
            roundn += 1
            prev_prob = log_prob
            log_prob = 0.0
            #for each sample with observations
            for a in range(len(values)):
                #set variables according to observations
                more_hid = []
                for b in range(len(labels)):
                    self.nodes[labels[b]].instance = values[a][b]
                    if self.nodes[labels[b]].instance is None:
                        # The observation is None, so we add this to our list
                        # of latent variables
                        more_hid.append(labels[b])
                #to hold the expectations for EM
                jpt = None
                #a "cache" for the EM-JPT
                p = None
                #If there are hidden variables, use EM
                if len(hid_labels) > 0 or len(more_hid) > 0:
                    latent_variable_exist = True
                    #find all names of latent variables
                    hid = hid_labels + more_hid
                    #we compute the expectations of latent variables on
                    #the basis of the current settings (E-step)
                    jpt = self.infer_naive(hid)
                    log_prob += jpt.log_likelihood()
                    jpt.normalize()
                    #pull out necessary data from inference
                    infkey = [entry(t, len(jpt.labels)) for t in range(jpt.maxrows)]
                    p = [jpt.get(infkey[c]) for c in range(len(infkey))]

                # FIXME: It's possible at this point that the JPT is None, if
                # there are no hidden variables. Does this case make sense in
                # a training context?

                #now go through each of BN nodes...
                jpt_lab_length = len(jpt.labels)
                p_length = len(p)
                for node in update:
                    if not node.trainable:
                        continue

                    parents = node.labels
                    variable = node.name
                    value = node.instance

                    #This is a prior, must be boolean
                    if len(parents) == 0:
                        #The value is set so no need to use expectations
                        if value is not None:
                            node.count_instance(None, value, 1.0)
                        else:  #ok this prior is hidden...
                            #We use the expectations to modify the node
                            for x in range(p_length):
                                # complete the key
                                infkey = entry(x, jpt_lab_length)
                                vindex = jpt.get_key_indices(variable)
                                if vindex != -1:
                                    node.count_instance(None, infkey[vindex], p[x])
                                else:
                                    raise RuntimeError("Incorrectly\
                                    specified evidence: " + variable)

                    #There are parent variables, either a CPT or CDT
                    else:
                        # Sort out what the boolean key should look like
                        key = [0] * len(parents)
                        myhid = {}
                        for d in range(len(parents)):
                            key[d] = self.nodes[parents[d]].instance
                            if key[d] is None:
                                myhid[jpt.get_key_indices(parents[d])] = d

                        # This node includes hidden variables; we must use EM
                        if len(myhid) > 0 or value is None:
                            #EM: we use the expectations to modify the node
                            for e in range(p_length):
                                infkey = entry(e, jpt_lab_length)
                                for k, v in myhid.iteritems():
                                    key[v] = infkey[k]
                                if value is None:
                                    vindex = jpt.get_key_indices(variable)
                                    if vindex != -1:
                                        node.count_instance(key, infkey[vindex], p[e])
                                    else:
                                        raise RuntimeError("Incompletely\
                                        specified evidence: " + variable)
                                else:
                                    node.count_instance(key, value, p[e])
                        #The key is already fixed, and no hidden variables
                        #don't use expectations
                        else:
                            node.count_instance(key, value, 1.0)

            # Complete the M-step by transferring counts to probabilities
            for node in update:
                if node.trainable:
                    node.maximize_instance()

            # Use absolute as joint probability may exceed 1, i.e., it's not normalised
            conv_rate = math.fabs(log_prob - prev_prob) if latent_variable_exist else 0

            if self.EM_DEBUG and roundn % 10 == 0:
                print "Completed %i rounds, L = %i" % (roundn, log_prob)

        # Reset network state
        for node in self.nodes.values():
            node.instance = None

        if self.EM_DEBUG:
            print "Completed %i rounds, L = %i,. DONE" % (roundn, log_prob)

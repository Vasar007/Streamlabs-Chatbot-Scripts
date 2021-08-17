# -*- coding: utf-8 -*-


"""
pymitter
Python port of the extended Node.js EventEmitter 2 approach providing
namespaces, wildcards and TTL.
"""

from time import time


class ScoreEventEmitter(object):
    """
    The EventEmitter class.

    - *wildcard*: When *True*, wildcards are used.
    - *new_listener*: When *True*, the "new_listener" event is emitted
      every time a new listener is registered with arguments
      *(func, event=None)*.
    - *max_listeners*: Maximum number of listeners per event. Negative
      values mean infinity.
    - *delimiter*: The delimiter to separate event namespaces. Event names have
      namespace support with each namspace being separated by a *delimiter*
    """

    __CBKEY = "__callbacks"
    __WCCHAR = "*"

    def __init__(self, wildcard=False, new_listener=False, max_listeners=-1,
                 delimiter="."):
        self.wildcard = wildcard
        self.new_listener = new_listener
        self.max_listeners = max_listeners
        self.delimiter = delimiter

        self._tree = self.__new_branch()

    @classmethod
    def __new_branch(cls):
        """
        Returns a new branch. Basically, a branch is just a dictionary with
        a special item *__CBKEY* that holds registered functions. All other
        items are used to build a tree structure.
        """
        return {cls.__CBKEY: []}

    def __find_branch(self, event):
        """
        Returns a branch of the tree structure that matches *event*. Wildcards
        are not applied.
        """
        parts = event.split(self.delimiter)

        if self.__CBKEY in parts:
            return None

        branch = self._tree
        for p in parts:
            if p not in branch:
                return None
            branch = branch[p]

        return branch

    @classmethod
    def __remove_listener(cls, branch, func):
        """
        Removes a listener given by its function from a branch.
        """
        listeners = branch[cls.__CBKEY]

        indexes = [i for i, l in enumerate(listeners) if l.func == func]

        for i in indexes[::-1]:
            listeners.pop(i)

    def on(self, event, func=None, ttl=-1):
        """
        Registers a function to an event. When *func* is *None*, decorator
        usage is assumed. *ttl* defines the times to listen. Negative values
        mean infinity. Returns the function.
        """
        def _on(func):
            if not callable(func):
                return func

            parts = event.split(self.delimiter)

            if self.__CBKEY in parts:
                return func

            branch = self._tree
            for p in parts:
                branch = branch.setdefault(p, self.__new_branch())

            listeners = branch[self.__CBKEY]

            if 0 <= self.max_listeners <= len(listeners):
                return func

            listener = ScoreListener(func, event, ttl)
            listeners.append(listener)

            if self.new_listener:
                self.emit("new_listener", func, event)

            return func

        return _on(func) if func else _on

    def once(self, event, func=None):
        """
        Registers a function to an event that is called once. When *func* is
        *None*, decorator usage is assumed. Returns the function.
        """
        return self.on(event, func=func, ttl=1)

    def on_any(self, func=None, ttl=-1):
        """
        Registers a function that is called every time an event is emitted.
        When *func* is *None*, decorator usage is assumed. Returns the
        function.
        """
        def _on_any(func):
            if not callable(func):
                return func

            listeners = self._tree[self.__CBKEY]

            if 0 <= self.max_listeners <= len(listeners):
                return func

            listener = ScoreListener(func, None, ttl)
            listeners.append(listener)

            if self.new_listener:
                self.emit("new_listener", func)

            return func

        return _on_any(func) if func else _on_any

    def off(self, event, func=None):
        """
        Removes a function that is registered to an event. When *func* is
        *None*, decorator usage is assumed. Returns the function.
        """
        def _off(func):
            branch = self.__find_branch(event)
            if branch is None:
                return func

            self.__remove_listener(branch, func)

            return func

        return _off(func) if func else _off

    def off_any(self, func=None):
        """
        Removes a function that was registered via *on_any*. When *func* is
        *None*, decorator usage is assumed. Returns the function.
        """
        def _off_any(func):
            self.__remove_listener(self._tree, func)

            return func

        return _off_any(func) if func else _off_any

    def off_all(self):
        """
        Removes all registered functions.
        """
        del self._tree
        self._tree = self.__new_branch()

    def listeners(self, event):
        """
        Returns all functions that are registered to an event. Wildcards are
        not applied.
        """
        branch = self.__find_branch(event)
        if branch is None:
            return []

        return [l.func for l in branch[self.__CBKEY]]

    def listeners_any(self):
        """
        Returns all functions that were registered using *on_any*.
        """
        return [l.func for l in self._tree[self.__CBKEY]]

    def listeners_all(self):
        """
        Returns all registered functions.
        """
        listeners = list(self._tree[self.__CBKEY])
        branches = list(self._tree.values())

        for b in branches:
            if not isinstance(b, dict):
                continue

            branches.extend(b.values())

            listeners.extend(b[self.__CBKEY])

        return [l.func for l in listeners]

    def emit(self, event, *args, **kwargs):
        """
        Emits an *event*. All functions of events that match *event* are
        invoked with *args* and *kwargs* in the exact order of their
        registration. Wildcards might be applied.
        """
        parts = event.split(self.delimiter)

        if self.__CBKEY in parts:
            return

        listeners = list(self._tree[self.__CBKEY])
        branches = [self._tree]

        for p in parts:
            _branches = []
            for branch in branches:
                for k, b in branch.items():
                    if k == self.__CBKEY:
                        continue
                    if k == p:
                        _branches.append(b)
                    elif self.wildcard and self.__WCCHAR in (p, k):
                        _branches.append(b)

            branches = _branches

        for b in branches:
            listeners.extend(b[self.__CBKEY])

        # Call listeners in the order of their registration time.
        for l in sorted(listeners, key=lambda l: l.time):
            l(*args, **kwargs)

        # Remove listeners whose ttl value is 0.
        for l in listeners:
            if l.ttl == 0:
                self.off(l.event, func=l.func)


class ScoreListener(object):
    """
    The Listener class.

    A simple event listener class that wraps a function *func* for a specific\
    *event* and that keeps track of the times to listen left.
    """

    def __init__(self, func, event, ttl):
        self.func = func
        self.event = event
        self.ttl = ttl

        # Store the registration time.
        self.time = time()

    def __call__(self, *args, **kwargs):
        """
        Invokes the wrapped function when ttl is non-zero, decreases the ttl
        value when positive and returns whether it reached zero or not.
        """
        if self.ttl != 0:
            self.func(*args, **kwargs)

        if self.ttl > 0:
            self.ttl -= 1

        return self.ttl == 0

class Split(object):
    def __repr__(self):
        return '<Split: expense: %s user: %s share: %s>' % (self.expenditure,
                                                            self.user,
                                                            self.share)

__all__ = ['Split']

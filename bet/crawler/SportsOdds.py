__author__ = 'tintsing'


class SportsOdds (object):
    def __init__(self):
        self.vendor = ''
        self.league = ''
        self.start_time = ''
        self.host = ''
        self.away = ''

        self.host_score = 0
        self.away_score = 0

        # let(odd/ou)_result: 1 for host win, 0 for draw, -1 for away
        self.let_odd_1 = 0.0
        self.let_odd_2 = 0.0
        self.let_condition = ''
        self.let_result = 0

        self.win_odd = 0.0
        self.draw_odd = 0.0
        self.lose_odd = 0.0
        self.odd_result = 0

         # over / under
        self.ou_1 = 0.0
        self.ou_2 = 0.0
        self.ou_score = -1.0
        self.ou_result = 0


class BasketballOdds (SportsOdds):
    def __init__(self):
        super(BasketballOdds, self).__init__()
        self.round_type = ''

        self.origin_host_odd = 0.0
        self.origin_away_odd = 0.0
        self.origin_let_score = 0.0
        self.origin_ou_score = 0.0

    def __unicode__(self):
        return u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
            self.league, self.round_type, self.start_time, self.host, self.away, self.host_score,
            self.away_score, self.origin_let_score, self.let_condition,self.origin_host_odd, self.origin_away_odd,
            self.win_odd, self.lose_odd, self. odd_result, self.origin_ou_score, self.ou_score
        )



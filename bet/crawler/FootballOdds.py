from SportsOdds import SportsOdds

__author__ = 'tintsing'

class FootballOdds (SportsOdds):
    def __init__(self):
        super(FootballOdds, self).__init__()

        self.host_rank = 0
        self.away_rank = 0

    def __unicode__(self):
         return u'%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
                (self.league, self.start_time, self.host,
                self.away, self.host_rank, self.away_rank, self.let_odd_1, self.let_odd_2, self.let_condition,
                self.win_odd, self.draw_odd, self.lose_odd, self.ou_1, self.ou_score, self.ou_2,
                self.host_score, self.away_score)




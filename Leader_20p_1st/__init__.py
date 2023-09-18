from otree.api import *
import random
from decimal import Decimal
author = 'Tran_Luu'

doc = """
A leader game with random leader. All start with 10 cu, the leader would have a flat earning 
and the members would have to 
invest a flat invest. The leader then can invest
 all the money from the member or embellish some for themselves. 
"""


class Constants(BaseConstants):
    name_in_url = 'Leader_20p_1st'
    players_per_group = 4
    num_rounds = 1
    endowment = cu(10) #cu() is currency for the game (ie, tokens)
    flat_earning = cu(5) #"b" in the model
    flat_invest = cu(4)  #"c" in the model

    prob = ['0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50',
           '55', '60', '65', '70', '75', '80', '85', '90', '95', '100']  # for the dropdown list the prob you think each teammate will take everything
    about = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']  #for the drop down list asking how much you think each teammate will steal from the group

    #return rates and probabilities of each investment portfolio (solutions to systems of eqs)
    r_A = 2.5
    r_B = 1.5
    r_C = 1
    r_D = 1
    r_E = 2
    p_A = 1
    p_B = 0.5
    p_C = 0.5
    p_D = 0.5
    p_E = 0.5
    #the systems of equations
    question_A_1 = '-10.5p + r = -8'
    question_A_2 = '1.5p + r = 4'
    question_B_1 = '-9.5p + 0.5r = -4'
    question_B_2 = '2.5p + 0.5r = 2'
    question_C_1 = '-6p + 0.5r = -2.5'
    question_C_2 = '5p + 0.5r = 3'
    question_D_1 = '-11p + 0.5r = -5'
    question_D_2 = '5p + 0.5r = 3'
    question_E_1 = '-13p + 0.5r = -5.5'
    question_E_2 = '10p + 0.5r = 6'
    #2 different orders for the portfolios to appear
    order = [1, 2, 3, 4, 5]
    order_2 =['E', 'D', 'C', 'B', 'A']



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    random_pick = models.IntegerField()
    invest = models.CurrencyField(initial=cu(0))
    take_for_myself = models.CurrencyField(initial=cu(0))
    rate = models.FloatField(initial=0)
    invest_B = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))
    invest_C = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))
    invest_D = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))
    invest_E = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))
    invest_A = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))


class Player(BasePlayer):
    rate = models.FloatField()
    rank = models.IntegerField()
    role_player = models.CharField()
    invest = models.CurrencyField(choices=currency_range(cu(0), Constants.flat_invest*3, cu(1)), initial=cu(0))
    take_for_myself = models.CurrencyField(choices=currency_range(cu(0), Constants.flat_invest*3, cu(1)), initial=cu(0))
    id_A = models.IntegerField()
    id_B = models.IntegerField()
    id_C = models.IntegerField()
    sent_A = models.CurrencyField()
    sent_B = models.CurrencyField()
    sent_C = models.CurrencyField()
    sent_back_A = models.CurrencyField()
    sent_back_B = models.CurrencyField()
    sent_back_C = models.CurrencyField()
#    trust_A = models.StringField()
#    trust_B = models.StringField()
#    trust_C = models.StringField()
    rate_A = models.FloatField()
    rate_B = models.FloatField()
    rate_C = models.FloatField()
    about_A = models.StringField(choices=Constants.about)
    about_B = models.StringField(choices=Constants.about)
    about_C = models.StringField(choices=Constants.about)
    prob_A = models.StringField(choices=Constants.prob)
    prob_B = models.StringField(choices=Constants.prob)
    prob_C = models.StringField(choices=Constants.prob)


    invest_B = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))
    invest_C = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))
    invest_D = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))
    invest_E = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))
    invest_A = models.CurrencyField(min=cu(0), max=Constants.flat_invest*3, initial=cu(0))
    answer_p_A = models.StringField(initial='', blank=True)
    answer_p_B = models.StringField(initial='', blank=True)
    answer_p_C = models.StringField(initial='', blank=True)
    answer_p_D = models.StringField(initial='', blank=True)
    answer_p_E = models.StringField(initial='', blank=True)
    answer_r_A = models.StringField(initial='', blank=True)
    answer_r_B = models.StringField(initial='', blank=True)
    answer_r_C = models.StringField(initial='', blank=True)
    answer_r_D = models.StringField(initial='', blank=True)
    answer_r_E = models.StringField(initial='', blank=True)
    r_p_A = models.FloatField()
    r_p_B = models.FloatField()
    r_p_C = models.FloatField()
    r_p_D = models.FloatField()
    r_p_E = models.FloatField()


#FUNCTIONS
def random_pick(subsession: Subsession):
    for group in subsession.get_groups():
        group.random_pick = random.randint(1, Constants.players_per_group)

def creating_group(subsession: Subsession):
    group_1 = []
    group_2 = []
    group_3 = []
    group_4 = []
    group_5 = []
    matrix = []
    for p in subsession.get_players():
        p.rank = p.participant.vars['rank'+str(p.participant.id_in_session)]
        if p.rank in [1, 6, 11, 16]:
            group_1.append(p)
        elif p.rank in [2, 7, 12, 17]:
            group_2.append(p)
        elif p.rank in [3, 8, 13, 18]:
            group_3.append(p)
        elif p.rank in [4, 9, 14, 19]:
            group_4.append(p)
        else:
            group_5.append(p)
    matrix.append(group_1)
    matrix.append(group_2)
    matrix.append(group_3)
    matrix.append(group_4)
    matrix.append(group_5)
    subsession.set_group_matrix(matrix)


def choose_leader(player: Player):
    if player.id_in_group == player.group.random_pick:
        player.role_player = 'Leader'
    else:
        player.role_player = 'Member'
    return player.role_player


def set_pay_off(player: Player):
    group_funds = player.group.invest
    if player.group.r_p_A <= Constants.p_A:
        group_funds += player.group.invest_A * (Constants.r_A - 1)
    if player.group.r_p_B <= Constants.p_B:
        group_funds += player.group.invest_B * (Constants.r_B - 1)
    if player.group.r_p_C <= Constants.p_C:
        group_funds += player.group.invest_C * (Constants.r_C - 1)
    if player.group.r_p_D <= Constants.p_D:
        group_funds += player.group.invest_D * (Constants.r_D - 1)
    if player.group.r_p_E <= Constants.p_E:
        group_funds += player.group.invest_E * (Constants.r_E - 1)

    if player.role_player == 'Leader':
        player.payoff = Constants.endowment + Constants.flat_earning + player.group.take_for_myself


    if player.role_player == 'Member':
        player.payoff = Constants.endowment - Constants.flat_invest +(group_funds)/3
    return player.payoff



#PAGES

class Instructions(Page):
    pass


class ShufflePage(WaitPage):
    title_text = 'Please wait for other participants to finish making decisions!'
    body_text = 'Thank you for your patience!'

    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        creating_group(subsession)
        random_pick(subsession)


class LeaderChoice(Page):
    form_model = 'player'
    form_fields = ['invest', 'take_for_myself']
    timeout_seconds = 300

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'c': Constants.flat_invest,
            '3c': Constants.flat_invest * 3
        }
    @staticmethod
    def error_message(player: Player, values):
        if values['invest'] + values['take_for_myself'] != Constants.flat_invest * 3:
            return 'The total amount must be equal to the group account'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.invest = cu(0)
            player.take_for_myself = cu(0)

## added a new page (copy/paste from invest section) for the player to choose how to invest the group fund
class Invest(Page):
    form_model = "player"
    form_fields = ['invest_A', 'invest_B', 'invest_C', 'invest_D', 'invest_E',
                   'answer_p_A', 'answer_p_B', 'answer_p_C', 'answer_p_D', 'answer_p_E',
                   'answer_r_A', 'answer_r_B', 'answer_r_C', 'answer_r_D', 'answer_r_E']
    timeout_seconds = 240

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['order2'] = Constants.order_2.copy()
        player.participant.vars[str(player.participant.id_in_session) + 'order'] = \
            random.sample(Constants.order, len(Constants.order))
        return {
                'A1': Constants.question_A_1,
                'A2': Constants.question_A_2,
                'B1': Constants.question_B_1,
                'B2': Constants.question_B_2,
                'C1': Constants.question_C_1,
                'C2': Constants.question_C_2,
                'D1': Constants.question_D_1,
                'D2': Constants.question_D_2,
                'E1': Constants.question_E_1,
                'E2': Constants.question_E_2,
                'order': player.participant.vars[str(player.participant.id_in_session)+'order'],
                'order_2': player.participant.vars['order2']
        }

    @staticmethod
    def error_message(player: Player, values):
        if values['invest_A'] + values['invest_B'] + values['invest_C'] + values['invest_D'] + \
                values['invest_E'] > player.invest:
            return 'The total amount invested must not be larger than the remaining group fund!'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.invest_A = cu(0)
            player.invest_B = cu(0)
            player.invest_C = cu(0)
            player.invest_D = cu(0)
            player.invest_E = cu(0)




class Trust(Page):
    form_model = 'player'
    form_fields = ['about_A', 'about_B', 'about_C', 'prob_A', 'prob_B', 'prob_C']
    timeout_seconds = 300

    @staticmethod
    def vars_for_template(player: Player):
        other_player_rate = []
#        other_player_trust = []
        other_player_sent = []
        other_player_sent_back = []
        other_player_id = []
        for other_player in player.get_others_in_group():
            other_player_sent.append(other_player.participant.vars
                                     ['round1' + str(other_player.participant.id_in_session) + 'sent_amount'])
            other_player_sent_back.append(other_player.participant.vars
                                          ['round1' + str(other_player.participant.id_in_session) + 'sent_back_amount'])
#            other_player_trust.append(other_player.participant.vars
#                                      ['round1' + str(other_player.participant.id_in_session) + 't'])
            other_player_rate.append(other_player.participant.vars
                                     ['rate' + str(other_player.participant.id_in_session)])
            other_player_id.append(other_player.participant.id_in_session)
#        player.trust_A = "{:.0f}".format(other_player_trust[0])
#        player.trust_B = "{:.0f}".format(other_player_trust[1])
#        player.trust_C = "{:.0f}".format(other_player_trust[2])
        player.rate_A = other_player_rate[0]
        player.rate_B = other_player_rate[1]
        player.rate_C = other_player_rate[2]
        player.sent_A = other_player_sent[0]
        player.sent_B = other_player_sent[1]
        player.sent_C = other_player_sent[2]
        player.sent_back_A = other_player_sent_back[0]
        player.sent_back_B = other_player_sent_back[0]
        player.sent_back_C = other_player_sent_back[0]
        player.id_A = other_player_id[0]
        player.id_B = other_player_id[1]
        player.id_C = other_player_id[2]
        return {
            'rateA': other_player_rate[0],
            'rateB': other_player_rate[1],
            'rateC': other_player_rate[2],
            'sentA': other_player_sent[0] * 3,
            'sentB': other_player_sent[1] * 3,
            'sentC': other_player_sent[2] * 3,
            'sent_backA': other_player_sent_back[0],
            'sent_backB': other_player_sent_back[1],
            'sent_backC': other_player_sent_back[2]
        }



class ResultWaitPage(WaitPage):
    title_text = 'Please wait for other participants to finish making decisions!'
    body_text = 'Thank you for your patience!'

    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():  #determines each player's status, then determines outcome vars for each group
            player.role_player = choose_leader(player)
            player.rate = player.participant.vars['rate'+str(player.participant.id_in_session)]
            if player.role_player == 'Leader':
                group.invest += player.invest
                group.take_for_myself += player.take_for_myself
                #group.rate += player.rate
                group.invest_B = player.invest_B
			    group.invest_C = player.invest_C
			    group.invest_D = player.invest_D
			    group.invest_E = player.invest_E
			    group.invest_A = player.invest_A
			    group.r_p_A = player.r_p_A
			    group.r_p_B = player.r_p_B
			    group.r_p_C = player.r_p_C
			    group.r_p_D = player.r_p_D
			    group.r_p_E = player.r_p_E



class Result(Page):

    @staticmethod
    def vars_for_template(player: Player):
        player.role_player = choose_leader(player)
        player.payoff = set_pay_off(player)
        player.participant.vars['round1' + str(player.participant.id_in_session) + 'leader_p'] = player.payoff
        return {
            'earning': player.payoff,
            'role': player.role_player
        }


page_sequence = [
    Instructions,
    ShufflePage,
    LeaderChoice,
    Invest,
    Trust,
    ResultWaitPage,
    Result
    ]







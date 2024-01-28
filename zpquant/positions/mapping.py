from zpquant.positions.calculators.neutral import DollarNeutral, BetaNeutral
from zpquant.positions.calculators.risk_adj import Grinold

weight_mapping = dict(dollar_neutral =  DollarNeutral,
                       beta_neutral =  BetaNeutral,
                        grinold = Grinold)
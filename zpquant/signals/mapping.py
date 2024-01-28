from zpquant.features.momentum.price_momentum import EQPriceMomentum, FUPriceMomentum
from zpquant.signals.calculators import RankSignal, ZscoreSignal, NormalizedSignal, RankSignalXS, RankSignalTS, ZscoreSignalTS, ZscoreSignalXS

feature_mapping = dict(EQPriceMomentum = EQPriceMomentum,
                      FUPriceMomentum = FUPriceMomentum)

signal_calculation_mapping = dict(rank = RankSignal,
                                rankTS = RankSignalTS,
                                zscoreTS = ZscoreSignalTS,
                                zscoreXS = ZscoreSignalXS,
                                rankXS = RankSignalXS,
                                zscore = ZscoreSignal,
                                normalized = NormalizedSignal)
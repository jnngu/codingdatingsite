structure Metrics1 = MkEitherMetric (structure M1 = LineMetric
                                     structure M2 = IndentMetric)
structure Metrics2 = MkEitherMetric (structure M1 = AverageLineLengthMetric
                                     structure M2 = MaxLineLengthMetric)
structure Metrics = MkEitherMetric (structure M1 = Metrics1
                                    structure M2 = Metrics2)
structure Metrics = MkEitherMetric (structure M1 = Metrics
                                    structure M2 = CaseMetric)

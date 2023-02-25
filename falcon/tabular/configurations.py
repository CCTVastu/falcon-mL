from falcon.tabular.pipelines import SimpleTabularPipeline
from falcon.tabular.learners import SuperLearner, OptunaLearner, PlainLearner
from falcon.tabular.learners.super_learner import _default_estimators
from falcon.tabular.models.hist_gbt import HistGradientBoostingClassifier, HistGradientBoostingRegressor

SUPER_LEARNER_DEFAULT_CONFIG =  {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": SuperLearner, 
            "learner_kwargs": {}
        }
    }

OPTUNA_LEARNER_DEFAULT_CONFIG = {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": OptunaLearner, 
            "learner_kwargs": {}
        }
    }

PLAIN_LEARNER_DEFAULT_CONFIG = {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": PlainLearner, 
            "learner_kwargs": {}
        }
    }

TABULAR_CLASSIFICATION_CONFIGURATIONS = {
    "SuperLearner.mini": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": SuperLearner, 
            "learner_kwargs": {
                "cv": 10, 
                "base_estimators": _default_estimators['tabular_classification']['mini']
            }
        }
    }, 

    "SuperLearner.mid": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": SuperLearner, 
            "learner_kwargs": {
                "cv": 5, 
                "base_estimators": _default_estimators['tabular_classification']['mid']
            }
        }
    },

    "SuperLearner.large": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": SuperLearner, 
            "learner_kwargs": {
                "cv": 3, 
                "base_estimators": _default_estimators['tabular_classification']['large']
            }
        }
    },

    "SuperLearner.xlarge": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": SuperLearner, 
            "learner_kwargs": {
                "cv": 3, 
                "base_estimators": _default_estimators['tabular_classification']['x-large']
            }
        }
    },

    "OptunaLearner.hgbt": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": OptunaLearner, 
            "learner_kwargs": {"model_class": HistGradientBoostingClassifier}
        }
    },

    "PlainLearner.hgbt": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": PlainLearner, 
            "learner_kwargs": {"model_class": HistGradientBoostingClassifier}
        }
    },

    "SuperLearner": SUPER_LEARNER_DEFAULT_CONFIG,
    "OptunaLearner": OPTUNA_LEARNER_DEFAULT_CONFIG,
    "PlainLearner": PLAIN_LEARNER_DEFAULT_CONFIG
 
}

TABULAR_REGRESSION_CONFIGURATIONS = {
    "SuperLearner.mini": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": SuperLearner, 
            "learner_kwargs": {
                "cv": 10, 
                "base_estimators": _default_estimators['tabular_regression']['mini']
            }
        }
    }, 

    "SuperLearner.mid": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": SuperLearner, 
            "learner_kwargs": {
                "cv": 5, 
                "base_estimators": _default_estimators['tabular_regression']['mid']
            }
        }
    },

    "SuperLearner.large": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": SuperLearner, 
            "learner_kwargs": {
                "cv": 3, 
                "base_estimators": _default_estimators['tabular_regression']['large']
            }
        }
    }, 

    "SuperLearner.xlarge": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": SuperLearner, 
            "learner_kwargs": {
                "cv": 3, 
                "base_estimators": _default_estimators['tabular_regression']['x-large']
            }
        }
    }, 

    "OptunaLearner.hgbt": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": OptunaLearner, 
            "learner_kwargs": {"model_class": HistGradientBoostingRegressor}
        }
    },

    "PlainLearner.hgbt": {
        "pipeline": SimpleTabularPipeline, 
        "extra_pipeline_options": {
            "learner": PlainLearner, 
            "learner_kwargs": {"model_class": HistGradientBoostingRegressor}
        }
    },
    
    "SuperLearner": SUPER_LEARNER_DEFAULT_CONFIG, 
    "OptunaLearner": OPTUNA_LEARNER_DEFAULT_CONFIG,
    "PlainLearner": PLAIN_LEARNER_DEFAULT_CONFIG
}
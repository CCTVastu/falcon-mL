from __future__ import annotations
from falcon.abstract import TaskManager, Pipeline
from falcon.tabular.pipelines.simple_tabular_pipeline import SimpleTabularPipeline
from .reporting import print_classification_report, print_regression_report
from falcon.tabular.utils import *
from falcon import types as ft
from typing import Union, Optional, List, Tuple, Type, Dict, Any
from numpy import typing as npt
import pandas as pd
from falcon.utils import print_, set_verbosity_level
from sklearn.model_selection import train_test_split
import os

class TabularTaskManager(TaskManager):
    """
    Default task manager for tabular data.
    """

    def __init__(
        self,
        task: str,
        data: Union[str, npt.NDArray, pd.DataFrame],  # TODO add support for Tuple[X, y]
        pipeline: Optional[Type[Pipeline]] = None,
        pipeline_options: Optional[Dict] = None,
        extra_pipeline_options: Optional[Dict] = None,
        features: Optional[ft.ColumnsList] = None,
        target: Optional[Union[str, int]] = None,
        **options: Any,
    ) -> None:
        """

        Parameters
        ----------
        task : str
            `tabular_classification` or `tabular_regression`
        data : Union[str, npt.NDArray, pd.DataFrame]
            Path to data file or pandas dataframe or numpy array.
        pipeline: Optional[Type[Pipeline]] 
            class to be used as pipeline, by default None
            if None, SimpleTabularPipeline will be used
        pipeline_options : Optional[Dict], optional
            Arguments to be passed to the pipeline, by default None.
            These options will overwrite the ones from `default_pipeline_options` attribute.
        extra_pipeline_options : Optional[Dict], optional
            Arguments to be passed to the pipeline, by default None.
            These options will be passed in addition to the ones from `default_pipeline_options` attribute.
            This argument is ignored if `pipeline_options` is not None.
        features : Optional[ft.ColumnsList], optional
            Names or indices of columns to be used as features, by default None.
            If None, all columns except the last one will be used.
            If `target` argument is not None, features should be passed explicitly as well.
        target : Optional[Union[str, int]], optional
            Name or index of column to be used as target, by default None.
            If None, the last column will be used as target.
            If `features` argument is not None, target should be specified explicitly as well.
        """
        print_(f"\nInitializing a new TabularTaskManager for task `{task}`")

        super().__init__(
            task=task,
            data=data,
            pipeline=pipeline,
            pipeline_options=pipeline_options,
            extra_pipeline_options=extra_pipeline_options,
            features=features,
            target=target,
        )

    def _prepare_data(
        self, data: Union[str, npt.NDArray, pd.DataFrame], training: bool = True
    ) -> Tuple[npt.NDArray, npt.NDArray, List[bool]]:
        """
        Initial data preparation. 
            1) Optional: read data from the specified location
            2) Split into features and targets. By default it is assumed that the last column is the target.
            3) Clean data
            4) Determine numerical and categorical features (create categorical mask).

        Parameters
        ----------
        data : Union[str, npt.NDArray, pd.DataFrame]
            Path to data file or pandas dataframe or numpy array.

        Returns
        -------
        Tuple[npt.NDArray, npt.NDArray, List[bool]]
            Tuple of features, target and categorical mask for features.
        """
        if isinstance(data, str):
            data = read_data(data)
        X, y = split_features(data, features=self.features, target=self.target)
        X, y = clean_data_split(X, y)
        mask: List[bool]
        if training:
            mask = get_cat_mask(X)
        else: 
            mask = []
        if len(y.shape) == 2:
            y = y.ravel()
        return X, y, mask

    @property
    def default_pipeline(self) -> Type[Pipeline]:
        """
        default pipeline class
        """

        return SimpleTabularPipeline

    @property
    def default_pipeline_options(self) -> Dict:
        """
        default options for pipeline
        """
        options = {"mask": self._data[2]}
        return options

    def train(self, pre_eval: bool = True, **kwargs: Any) -> TabularTaskManager:
        """
        Invokes the training procedure of an underlying pipeline. Print an expected model performance if available.

        Parameters
        ----------
        pre_eval : bool, optional
            If True, first estimate model perfromance via 10 folds CV for small datasets or 25% test split for large datasets, by default True

        Returns
        -------
        TabularTaskManager
            self
        """
        if pre_eval:
            print_("Beginning training")

            print_("Pre-evaluation of model performance")
            # TODO make `no_print` context manager
            old_verbosity_level = int(os.getenv("FALCON_VERBOSITYLEVEL", "1"))
            set_verbosity_level(0)
            if (
                self._data[0].shape[0] * self._data[0].shape[1] < 50000
                or self._data[0].shape[0] < 500
            ):
                score = tab_cv_score(
                    self._pipeline, self._data[0], self._data[1], self.task
                )
                avg_score = float(np.mean(score))
            else:
                X_train, X_test, y_train, y_test = train_test_split(
                    self._data[0], self._data[1], test_size=0.25
                )
                copied_pipeline = deepcopy(self._pipeline)
                copied_pipeline.fit(X_train, y_train)
                pred = copied_pipeline.predict(X_test)
                avg_score = calculate_model_score(y_test, pred, self.task)
            set_verbosity_level(old_verbosity_level)
        print_("Beginning the main training phase")
        self._pipeline.fit(self._data[0], self._data[1])
        print_("Finished training")
        if pre_eval:
            print(f"Score: {avg_score}")
        return self

    def predict(self, data: Union[str, npt.NDArray, pd.DataFrame]) -> npt.NDArray:
        """
        Perform prediction on new data.

        Parameters
        ----------
        data : Union[str, npt.NDArray, pd.DataFrame]
             Path to data file or pandas dataframe or numpy array.

        Returns
        -------
        npt.NDArray
            predictions
        """
        if isinstance(data, str):
            data = read_data(data)
        if not isinstance(data, np.ndarray):
            data = np.asarray(data, dtype=np.object_)
        return self._pipeline.predict(data)

    def predict_train_set(self) -> npt.NDArray:
        """
        Obtain predictions on the train set.

        Returns
        -------
        npt.NDArray
            predictions
        """
        return self.predict(self._data[0])


    def evaluate(self, test_data: Union[str, npt.NDArray, pd.DataFrame]) -> None:
        """
        Perfoms and prints the evaluation report on the given dataset.

        Parameters
        ----------
        test_data : Union[str, npt.NDArray, pd.DataFrame]
            Dataset to be used for evaluation.
        """
        print("The evaluation report will be provided here")
        X, y, _ = self._prepare_data(test_data, training = False)
        y_hat = self.predict(X)
        if self.task == "tabular_classification":
            print_classification_report(y, y_hat)
        else:
            print_regression_report(y, y_hat)
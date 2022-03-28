import pandas as pd
from pandas.testing import assert_frame_equal
from coffee_records_functions import getMainMap, getTable, getVehicleMapPlot, searchRecords

#Tests for main functions, all should pass.
def runTests():
    test1Dataframe=pd.read_parquet('test1.parquet', engine='pyarrow')
    test2Dataframe=pd.read_parquet('test2.parquet', engine='pyarrow')

    assert_frame_equal(test1Dataframe,searchRecords("oh"))
    assert_frame_equal(test2Dataframe,searchRecords("new"))
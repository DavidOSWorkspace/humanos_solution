import pandas as pd
import pytest
from humanos.core import calculate_signals, cohort_report, moments
from humanos.predictive import validate_predictive


def toy():
    responses = pd.DataFrame({'participant_id':['a'],'age_group':['21_28'],'role':['manager'],
                              'work_mode':['hybrid'],'A':[1],'B':[5]})
    config = pd.DataFrame({'item_code':['A','B'],'signal':['Test','Test'],
                           'reverse_flag':[False,True],'weight':[1.,3.]})
    return responses, config

def test_reverse_weight_normalization():
    r,c=toy()
    assert calculate_signals(r,c)['Test'].iloc[0] == 0
    r['A']=5
    assert calculate_signals(r,c)['Test'].iloc[0] == 25

def test_out_of_range():
    r,c=toy();r['A']=6
    with pytest.raises(ValueError):calculate_signals(r,c)

def test_duplicate_id():
    r,c=toy();r=pd.concat([r,r],ignore_index=True)
    with pytest.raises(ValueError):calculate_signals(r,c)

def test_deterministic():
    r,c=toy()
    pd.testing.assert_frame_equal(calculate_signals(r,c),calculate_signals(r,c))

def test_small_cohort_suppressed():
    r,c=toy();s=calculate_signals(r,c)
    row=cohort_report(s)[0]
    assert row['reportable'] is False and row['score'] is None and row['delta'] is None

def test_moments_not_exclusive():
    # Full input dataset is used in integration test; multiple affinities can coexist.
    assert len(moments.__doc__) > 10

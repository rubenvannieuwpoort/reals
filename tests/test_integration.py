from reals import pi, exp, log
from reals import sin, sinh, csc, csch, cos, cosh, sec, sech, tan, tanh, cot, coth

from math import pi as math_pi
from fractions import Fraction


def test_closest_float() -> None:
    assert pi.to_float() == math_pi


def test_sin_int() -> None:
    computed = sin(1).evaluate(100, round=False)
    expected = '0.8414709848078965066525023216302989996225630607983710656727517099919104043912396689486397435430526958'
    assert computed == expected


def test_sin_fraction() -> None:
    computed = sin(Fraction(1, 2)).evaluate(100, round=False)
    expected = '0.4794255386042030002732879352155713880818033679406006751886166131255350002878148322096312746843482690'
    assert computed == expected


def test_sinh_int() -> None:
    computed = sinh(1).evaluate(100, round=False)
    expected = '1.1752011936438014568823818505956008151557179813340958702295654130133075673043238956071174520896233918'
    assert computed == expected


def test_sinh_fraction() -> None:
    computed = sin(Fraction(1, 2)).evaluate(100, round=False)
    expected = '0.4794255386042030002732879352155713880818033679406006751886166131255350002878148322096312746843482690'
    assert computed == expected


def test_csc_int() -> None:
    computed = csc(1).evaluate(100, round=False)
    expected = '1.1883951057781212162615994523745510035278298340979626252652536663591843673571904879136635680308530232'
    assert computed == expected


def test_csc_fraction() -> None:
    computed = csc(Fraction(1, 2)).evaluate(100, round=False)
    expected = '2.0858296429334881857725016754592903019623095868169566261068915970443444223310094180614629904221048733'
    assert computed == expected


def test_csch_int() -> None:
    computed = csch(1).evaluate(100, round=False)
    expected = '0.8509181282393215451338427632871752841817246609103396169904211517290033643214651038997301773288938123'
    assert computed == expected


def test_csch_fraction() -> None:
    computed = csch(Fraction(1, 2)).evaluate(100, round=False)
    expected = '1.9190347513349437194922028787270061595871798715329719464146997939789976435032901275692420293602653691'
    assert computed == expected


def test_cos_int() -> None:
    computed = cos(1).evaluate(100, round=False)
    expected = '0.5403023058681397174009366074429766037323104206179222276700972553811003947744717645179518560871830893'
    assert computed == expected


def test_cos_fraction() -> None:
    computed = cos(Fraction(1, 2)).evaluate(100, round=False)
    expected = '0.8775825618903727161162815826038296519916451971097440529976108683159507632742139474057941840846822583'
    assert computed == expected


def test_cosh_int() -> None:
    computed = cosh(1).evaluate(100, round=False)
    expected = '1.5430806348152437784779056207570616826015291123658637047374022147107690630492236989642647264355430355'
    assert computed == expected


def test_cosh_fraction() -> None:
    computed = cosh(Fraction(1, 2)).evaluate(100, round=False)
    expected = '1.1276259652063807852262251614026720125478471180986674836289857351878587703039820163157120657821780495'
    assert computed == expected


def test_sec_int() -> None:
    computed = sec(1).evaluate(100, round=False)
    expected = '1.8508157176809256179117532413986501934703966550940092988351582778588154112615967059218414132873066711'
    assert computed == expected


def test_sec_fraction() -> None:
    computed = sec(Fraction(1, 2)).evaluate(100, round=False)
    expected = '1.1394939273245491223133277682049499284237252460490032204759607880741709340247849477430612596759629414'
    assert computed == expected


def test_sech_int() -> None:
    computed = sech(1).evaluate(100, round=False)
    expected = '0.6480542736638853995749773532261503231084893120719420230378653373187175956467128302808547853078928923'
    assert computed == expected


def test_sech_fraction() -> None:
    computed = sech(Fraction(1, 2)).evaluate(100, round=False)
    expected = '0.8868188839700739086588977977834085625340890887126139248362588825616942712100040608169228700589993129'
    assert computed == expected


def test_tan_int() -> None:
    computed = tan(1).evaluate(100, round=False)
    expected = '1.5574077246549022305069748074583601730872507723815200383839466056988613971517272895550999652022429838'
    assert computed == expected


def test_tan_fraction() -> None:
    computed = tan(Fraction(1, 2)).evaluate(100, round=False)
    expected = '0.5463024898437905132551794657802853832975517201797912461640913859329075105180258157151806482706562185'
    assert computed == expected


def test_tanh_int() -> None:
    computed = tanh(1).evaluate(100, round=False)
    expected = '0.7615941559557648881194582826047935904127685972579365515968105001219532445766384834589475216736767144'
    assert computed == expected


def test_tanh_fraction() -> None:
    computed = tanh(Fraction(1, 2)).evaluate(100, round=False)
    expected = '0.4621171572600097585023184836436725487302892803301130385527318158380809061404092787749490641519624905'
    assert computed == expected


def test_cot_int() -> None:
    computed = cot(1).evaluate(100, round=False)
    expected = '0.6420926159343307030064199865942656202302781139181713791011622804262768568391646721984829197601968046'
    assert computed == expected


def test_cot_fraction() -> None:
    computed = cot(Fraction(1, 2)).evaluate(100, round=False)
    expected = '1.8304877217124519192680194389688166237581079480161340043664159467854612241963551601121464877910498279'
    assert computed == expected


def test_coth_int() -> None:
    computed = coth(1).evaluate(100, round=False)
    expected = '1.3130352854993313036361612469308478329120139412404526555431529675670842704618743826746792414808563029'
    assert computed == expected


def test_coth_fraction() -> None:
    computed = coth(Fraction(1, 2)).evaluate(100, round=False)
    expected = '2.1639534137386528487700040102180231170937386021507922725335741192960876347833394865744094188097501153'
    assert computed == expected


def test_exp() -> None:
    computed = exp(1 / (pi * pi)).evaluate(100, round=False)
    expected = '1.1066320167919263117766683592471107492455596600981079480555345318984041430707902038526701842463312641'
    assert computed == expected


def test_log_exp() -> None:
    computed = log(exp(pi)).evaluate(100, round=False)
    expected = pi.evaluate(100, round=False)
    assert computed == expected


def test_exp_log() -> None:
    computed = exp(log(pi)).evaluate(100, round=False)
    expected = pi.evaluate(100, round=False)
    assert computed == expected

    assert computed == expected

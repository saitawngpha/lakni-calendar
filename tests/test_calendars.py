import datetime
import pathlib
import sys
import unittest


RESEARCH_DIR = pathlib.Path(__file__).resolve().parents[1] / "lak_ni_research"
sys.path.insert(0, str(RESEARCH_DIR))

import lak_jeng  # noqa: E402
import lak_ni  # noqa: E402
import sakkaraj  # noqa: E402


class AhomLakniTests(unittest.TestCase):
    """Anchors from Kapoor 2021, Tables 7-9 and pp. 668, 686-687."""

    def test_canonical_table_positions(self):
        expected = {
            1: "Kap Cheu",
            7: "Khut Shinga",
            18: "Rung Shiu",
            26: "Kat Plao",
            43: "Rai Shinga",
            60: "Ka Keu",
        }
        for position, name in expected.items():
            self.assertEqual(lak_ni.AHOM_LAKNI_60[position - 1], name)

    def test_2008_cycle_restart_and_2026_date(self):
        start = sakkaraj.jdn_to_gregorian(lak_ni.ahom_new_year_jdn(2008))
        on_start = lak_ni.ahom_lakni_for_date(start.year, start.month, start.day)
        self.assertEqual((on_start["position"], on_start["name"]), (1, "Kap Cheu"))

        result = lak_ni.ahom_lakni_for_date(2026, 8, 23)
        self.assertEqual((result["position"], result["name"]), (18, "Rung Shiu"))
        self.assertEqual(result["start_date"], datetime.date(2025, 11, 20))

    def test_report_separates_ahom_and_chinese_comparison(self):
        report = lak_ni.full_report(2026, 8, 23)
        self.assertIn("Ahom Lakni     : 18/60 Rung Shiu", report)
        self.assertIn("Ganzhi compare : Rai-Singa", report)
        self.assertNotIn("folk Me-Pi", report)


class MyanmarCalendarTests(unittest.TestCase):
    """Regression anchors from Yan Naing Aye's MIT-licensed mmcal implementation."""

    def test_exception_years(self):
        expected = {
            1263: "big watat",
            1264: "common",
            1344: "little watat",
            1345: "common",
            1377: "big watat",
        }
        for year, prefix in expected.items():
            self.assertTrue(sakkaraj.watat_type(year)["type"].startswith(prefix))

    def test_published_second_waso_anchors(self):
        self.assertEqual(sakkaraj.watat_type(1374)["waso_fm"], 2456142)
        self.assertEqual(sakkaraj.watat_type(1377)["waso_fm"], 2457235)
        self.assertEqual(sakkaraj.jdn_to_gregorian(2457235), datetime.date(2015, 7, 31))

    def test_myanmar_round_trips_across_eras(self):
        samples = [
            (205, 4, 15),
            (813, 9, 1),
            (1120, 4, 15),
            (1263, 0, 1),
            (1344, 9, 1),
            (1387, 9, 1),
        ]
        for my, month, day in samples:
            jdn = sakkaraj.myanmar_to_jdn(my, month, day)
            converted = sakkaraj.jdn_to_myanmar(jdn)
            self.assertEqual((converted["my"], converted["month"], converted["month_day"]),
                             (my, month, day))

    def test_dynamic_solar_new_year_boundary(self):
        self.assertEqual(sakkaraj.cs_year_for(2015, 4, 16), 1376)
        self.assertEqual(sakkaraj.cs_year_for(2015, 4, 17), 1377)


class LakJengTests(unittest.TestCase):
    def test_shan_year_2120_boundary(self):
        self.assertEqual(lak_jeng.tai_new_year_jdn(2025), lak_jeng.to_jdn(2025, 11, 20))
        self.assertEqual(lak_jeng.tai_year_from_gregorian(2025, 11, 19), 2119)
        self.assertEqual(lak_jeng.tai_year_from_gregorian(2025, 11, 20), 2120)

    def test_source_discrepancy_remains_explicit(self):
        self.assertEqual(lak_jeng.calculate(2116)["a"], 772531)
        self.assertEqual(lak_jeng.a_for_date(2021, 12, 5), 772521)
        self.assertEqual(lak_jeng.calculate(2116)["a"] -
                         lak_jeng.a_for_date(2021, 12, 5), 10)

    def test_market_day_label_matches_indices(self):
        for offset in range(10):
            dt = datetime.date(2026, 8, 23) + datetime.timedelta(days=offset)
            report = lak_jeng.report_date(dt.year, dt.month, dt.day)
            idx = lak_jeng.day_index_from_a(lak_jeng.a_for_date(dt.year, dt.month, dt.day))
            self.assertEqual("market day      : yes" in report, idx % 10 in (2, 7))


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""PF01 documented-structure and illustrative probes ONLY; not published numerical replication.
Runs without external PDF, validates committed A/B/C/D receipts and source-grounded toy counterfactuals.
The original v2.3.1 scientific validator has not been imported and is NOT invoked here.
"""
import hashlib
import json
import math
import random
import subprocess
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE_SHA = "8531103d577a3249c7edffa06ef2a8a7e85eb01b0a2f02cee2145e187581fbc3"
FILES = {
    "pre_a": ("PF01_PRE_A_REQUALIFIED_20261004.json", "9a9e72d7d0174af1fe9623c15874fbe6fe1a91ba2836312bbad652ab9c294f7b"),
    "A": ("PF01_A_ORIGINAL_SOURCE_20261004.json", "79e308cd97ec01bc2456d636422fd66b6279681ff631948959d294f1482c6383"),
    "B": ("PF01_B_RESULT_INFORMED_20261004.json", "8baa554cefc97bd773fff78dffb903275e96943a6a9af645f0d81783f6b4f128"),
    "C": ("PF01_C_V231_SOURCE_CLOSED_20261004.json", "051fa6128cb384338a1767a9a78f6c64ea29eeb63eea9e26e8572368601d6d60"),
    "D": ("PF01_D_GRAMMAR_V0_RECONSTRUCTION_20261004.json", "db0e4652e8fb19900908dce7b48b70a3275e8872d98ff21599c21bdaaec2e8b8"),
}
LOCK_COMMITS = [
    "4203bedf35cd7d5f1d414f2f997b97731fdbe40a",
    "2cf93d7c7564a5156dadefb639b9c3fdf52ae207",
    "1850085fc913ec9f536a15f66a10f028a51f13fd",
    "9db4c66fdc8032981dd7890a590c1bfb356bdc54",
    "262fdde0febe8076e979b20885a816b2eb6709c7",
]

def load(key):
    return json.loads((HERE / FILES[key][0]).read_text(encoding="utf-8"))

def wrap(phi):
    return (phi + math.pi) % (2 * math.pi) - math.pi

def illustrative_sde_step(phi, drift, B, dt, gaussian):
    return wrap(phi + dt * drift + math.sqrt(dt * B) * gaussian)

def illustrative_rate_derivatives(s, u, x, phi, U, tau_s, tau_u, tau_x):
    return (-s/tau_s + u*x*phi,
            (U-u)/tau_u + U*(1-u)*phi,
            (1-x)/tau_x - u*x*phi)

class MetadataAndReportedStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a, cls.b, cls.c, cls.d = map(load, ("A", "B", "C", "D"))

    def test_sha_pins_against_real_repository_bytes(self):
        for name, (filename, sha) in FILES.items():
            with self.subTest(stage=name):
                raw = (HERE / filename).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), sha)
                sidecar = HERE / filename.replace(".json", ".sha256")
                self.assertEqual(sidecar.read_text().split()[0], sha)

    def test_source_stays_same_across_stage_artifacts(self):
        self.assertEqual(load("pre_a")["one_frozen_primary_source"]["sha256"], SOURCE_SHA)
        self.assertEqual(self.a["source"]["sha256"], SOURCE_SHA)
        self.assertEqual(self.b["input"]["same_primary_pdf_sha256"], SOURCE_SHA)
        self.assertEqual(self.c["primary_source_sha256"], SOURCE_SHA)
        self.assertEqual(self.d["inputs"]["original_publisher_pdf_sha256"], SOURCE_SHA)

    def test_git_chronology_frozen_separately(self):
        # Main uses squash-only merge. The immutable stage commits MUST remain
        # reachable via a dedicated long-lived audit ref even after PR branch deletion.
        # CI uses checkout fetch-depth: 0 so remote refs are available.
        anchor = "refs/remotes/origin/audit/p399-pf01-chronology-20261004"
        expected = "21ca1cbae4d27bb22e54cfe7816fbd11a6588cf7"
        p = subprocess.run(["git", "rev-parse", "--verify", anchor], cwd=REPO,
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, "Missing permanent PF01 audit branch; fetch full history")
        self.assertEqual(p.stdout.strip(), expected, "Frozen audit ref moved: STOP")
        for older, newer in zip(LOCK_COMMITS, LOCK_COMMITS[1:]):
            with self.subTest(older=older, newer=newer):
                p = subprocess.run(["git", "merge-base", "--is-ancestor", older, newer],
                                   cwd=REPO, capture_output=True)
                self.assertEqual(p.returncode, 0, (older, newer, p.stderr.decode(errors="replace")))

    def test_original_A_complete_id_coverage_in_B(self):
        for items, a_items in (("per_original_A_claim", "claims"),
                               ("per_original_A_node", "typed_nodes"),
                               ("per_original_A_edge", "typed_edges")):
            self.assertEqual({x["original_id"] for x in self.b[items]},
                             {x["id"] for x in self.a[a_items]})
        self.assertEqual([s["section_id"] for s in self.b["original_source_order_coverage"]],
                         [s["id"] for s in self.a["source_order_coverage"]])

    def test_all_B_objections_get_one_C_disposition(self):
        self.assertEqual({x["id"] for x in self.b["findings"]},
                         {x["id"] for x in self.c["c1_source_vs_entire_original_A_objection_adjudication"]})
        self.assertEqual(len(self.b["findings"]), 12)
        self.assertTrue(all(x["c1_full_original_A_reopened_before_any_patch"]
                            for x in self.c["c1_source_vs_entire_original_A_objection_adjudication"]))

    def test_C1_reject_duplicate_and_only_patch_gaps(self):
        decisions = self.c["c1_source_vs_entire_original_A_objection_adjudication"]
        for x in decisions:
            self.assertEqual(x["patch"] is not None, x["c1_gap_test"] == "SOURCE_GAP_CONFIRMED")
        self.assertEqual({x["id"] for x in decisions if x["patch"]},
                         {"B01", "B02", "B03", "B12"})
        self.assertEqual({p["origin"] for p in self.c["append_only_delta"]},
                         {"B01", "B02", "B03", "B12"})

    def test_C2_unique_material_conditions_and_full_sweep(self):
        cs = self.c["c2_material_conditions_once_each"]
        self.assertEqual(len(cs), 16)
        self.assertEqual({x["id"] for x in cs}, {x["id"] for x in self.a["material_limits"]})
        self.assertTrue(all(x["treatment"] == "ALREADY_IN_A" and x["c2_context_checked"]
                            for x in cs))
        self.assertEqual(len(self.c["complete_independent_C_source_order_resweep"]), 16)
        self.assertEqual(sum(x["zero_B"] for x in self.c["complete_independent_C_source_order_resweep"]), 8)

    def test_source_variants_not_silently_collapsed(self):
        self.assertEqual(len(self.a["typed_nodes"]), 25)
        self.assertEqual(len(self.a["typed_edges"]), 33)
        x = self.d["layers"]["L_formal"]
        self.assertIn("full_spiking", x)
        self.assertIn("full_rate", x)
        self.assertIn("reduction", x)
        self.assertEqual(self.d["corrected_A_node_and_edge_inventory"]["corrected_nodes"], 29)
        self.assertEqual(self.d["corrected_A_node_and_edge_inventory"]["corrected_edges"], 41)

    def test_gamma_not_K_and_no_external_recurrence_invented(self):
        w = self.d["system_world_experiment"]
        self.assertIn("NOT_SOURCE_JUSTIFIED", w["nonprimitive_system_world_coupled_recurrence"])
        self.assertIn("Gamma_in", w)
        self.assertIn("Gamma_out", w)
        self.assertFalse(self.d["layers"]["L_sys"]["Q"]["endogenous_system_Q_required"])

    def test_append_only_width_link_and_negative_cases(self):
        patches = {p["id"]: p for p in self.c["append_only_delta"]}
        self.assertIn("E34", {e["id"] for e in patches["P01"]["appended_edges"]})
        mutant = [{k: v for k, v in p.items()} for p in self.c["append_only_delta"]]
        mutant[0] = {**mutant[0], "appended_edges": []}
        self.assertNotIn("E34", {e["id"] for p in mutant for e in p["appended_edges"]})
        self.assertIn("L10", {x["id"] for x in self.c["c2_material_conditions_once_each"]})

class IllustrativeCounterfactuals(unittest.TestCase):
    def test_rate_STP_both_u_and_x_change_effective_synaptic_drive(self):
        ds, du, dx = illustrative_rate_derivatives(.2, .3, .8, 4.0, .2, .05, .4, .2)
        self.assertAlmostEqual(ds, -.2/.05+.3*.8*4)
        self.assertNotAlmostEqual(ds, -.2/.05+.8*4)  # destructive u-removal
        self.assertNotAlmostEqual(ds, -.2/.05+.3*4)  # destructive x-removal
        self.assertNotAlmostEqual(du, dx)

    def test_U_one_is_nonfacilitating_under_u_one(self):
        _, du, _ = illustrative_rate_derivatives(.2, 1., .8, 4., 1., .05, .4, .2)
        self.assertAlmostEqual(du, 0)

    def test_zero_firing_recovers_stp_with_distinct_time_constants(self):
        ds, du, dx = illustrative_rate_derivatives(.2, .4, .5, 0., .2, .05, .4, .2)
        self.assertLess(ds, 0)
        self.assertLess(du, 0)
        self.assertGreater(dx, 0)

    def test_spike_prearrival_update_not_post_facilitation_depletion(self):
        U, u_minus, x_minus = .2, .3, .8
        u_plus = u_minus + U*(1-u_minus)
        x_plus = x_minus - u_minus*x_minus  # source Eq29 PRE-arrival efficacy
        s_increment = u_minus*x_minus  # source Eq31 PRE-arrival efficacy
        self.assertAlmostEqual(u_plus, .44)
        self.assertAlmostEqual(x_plus, .56)
        self.assertAlmostEqual(s_increment, .24)
        self.assertNotAlmostEqual(x_plus, x_minus*(1-u_plus))  # destructive misordering

    def test_periodic_reduced_evolution_and_zero_B_no_randomness(self):
        self.assertTrue(-math.pi <= wrap(3.5) < math.pi)
        self.assertEqual(illustrative_sde_step(.5, 0., 0., .1, 3.),
                         illustrative_sde_step(.5, 0., 0., .1, -1.))
        for x in (100., -100., 20.):
            self.assertTrue(-math.pi <= wrap(x) < math.pi)

    def test_noise_B_is_variance_driver_in_small_time_toy(self):
        rnd = random.Random(20261004)
        gaussian = [rnd.gauss(0,1) for _ in range(1000)]
        low = [illustrative_sde_step(0., 0., .01, .1, z) for z in gaussian]
        high = [illustrative_sde_step(0., 0., .04, .1, z) for z in gaussian]
        vl = sum(t*t for t in low)/len(low)
        vh = sum(t*t for t in high)/len(high)
        self.assertAlmostEqual(vh/vl, 4., places=8)

    def test_directed_drift_counterfactual(self):
        phi=.6; dt=.1
        stable=illustrative_sde_step(phi, -.15*math.sin(phi), 0., dt, 0.)
        wrong_sign=illustrative_sde_step(phi, +.15*math.sin(phi), 0., dt, 0.)
        self.assertLess(abs(stable), abs(phi))
        self.assertGreater(abs(wrong_sign), abs(phi))

    def test_source_Eq11_additive_not_RSS(self):
        drift_rms, B, T = .2, .09, 1.
        source = drift_rms*T + math.sqrt(B*T)
        destroyed = math.sqrt((drift_rms*T)**2 + B*T)
        self.assertAlmostEqual(source, .5)
        self.assertNotAlmostEqual(source, destroyed)
        self.assertIn("ADDED", self.d_eq11_text())

    @staticmethod
    def d_eq11_text():
        return load("D")["layers"]["L_formal"]["source_derived_measure"]

if __name__ == "__main__":
    print("PF01: structural metadata and ILLUSTRATIVE model probes; not original numeric/empirical replication")
    unittest.main(verbosity=2)

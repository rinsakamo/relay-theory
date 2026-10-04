#!/usr/bin/env python3
"""PF03 supplementary actual author-code unit-level verification.

The pinned 2023-12-18 author Git tree is a SECONDARY IMPLEMENTATION SOURCE, never
a replacement for the selected 2024 original PDF and never original numeric replication.
This test executes original author model.inf unchanged on tiny synthetic inputs.
"""
from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
import types
import unittest
from pathlib import Path

import torch

HERE=Path(__file__).resolve().parent
AUTHOR=Path(sys.argv[0]).resolve().parent.parent/"_pf03_author_checkout"
AUTHOR_SHA="017556566a0e5eb4a76455b85371737c16fe9b0a"
ORIGINAL_BLOBS={
    "models/pc_three.py":"ecfb1d25ba38bebf5dcf477832166e1a59b389de",
    "experiments/three/params.json":"ccbdbbf223916b3340a787f3e7fc8a9e74c1926f",
    "analysis/err_dist.ipynb":"394aeb3238fa67279c6da45b7d6077e6bb939605",
}
# The original module uses utils only in its optional inf_first_step call. A
# minimal dependency stub avoids installing/reimplementing the paper's CLI
# training/plotting environment; we execute original inf() unchanged.
utils_stub=types.ModuleType("utils")
utils_stub.requires_grad=lambda params,flag:[p.requires_grad_(flag) for p in params]
sys.modules["utils"]=utils_stub
spec=importlib.util.spec_from_file_location("pf03_pinned_author_pc_three",AUTHOR/"models/pc_three.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class PF03ActualPinnedAuthorCodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def git(*args):
            return subprocess.check_output(["git","-C",str(AUTHOR),*args],text=True).strip()
        cls.git=staticmethod(git)
    def test_01_commit_and_exact_author_blobs(self):
        self.assertEqual(self.git("rev-parse","HEAD"),AUTHOR_SHA)
        for p,sha in ORIGINAL_BLOBS.items():
            self.assertTrue((AUTHOR/p).is_file())
            self.assertEqual(self.git("hash-object",p),sha)
    def test_02_original_preprint_parameter_and_notebook_measure(self):
        config=json.loads((AUTHOR/"experiments/three/params.json").read_text())
        self.assertEqual(config["thres"],0.73)
        notebook=json.loads((AUTHOR/"analysis/err_dist.ipynb").read_text())
        cells=[c["source"] for c in notebook["cells"] if c["cell_type"]=="code"]
        code="\n".join(("".join(c) if isinstance(c,list) else c) for c in cells)
        self.assertIn("R2_loss[:,1:]",code)
        self.assertIn("X.cdf(0.73)",code)
        self.assertIn("r2_loss[lst[b], t-1] > 0.73",code)
        self.assertIn(r"\Vert\hat{\mathbf{r}}^{(1)}_t - \bar{\mathbf{r}}^{(1)}_t\Vert_2^2",code)
    def test_03_primary_eq37_event_trigger_compared_with_pinned_author_ast(self):
        import ast
        body=(AUTHOR/"models/pc_three.py").read_text()
        a=ast.parse(body)
        cls=next(x for x in a.body if isinstance(x,ast.ClassDef) and x.name=="DynPredNet")
        forward=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=="forward")
        inf=next(x for x in cls.body if isinstance(x,ast.FunctionDef) and x.name=="inf")
        fsrc=ast.get_source_segment(body,forward)
        isrc=ast.get_source_segment(body,inf)
        self.assertIn("large_error_idx = r2_loss > self.thres",fsrc)
        self.assertIn("self.inf_second(large_error_idx",fsrc)
        self.assertIn("r2[large_error_idx]",fsrc)
        self.assertIn("r3[large_error_idx]",fsrc)
        self.assertIn("orig_r2 = r2.clone().detach()",isrc)
        self.assertIn("self.temporal_prediction_one_(r_p, orig_r2).clone().detach()",isrc)
        self.assertIn("r2_loss = torch.pow(",isrc)
        self.assertIn(".sum(1)",isrc)
    def test_04_execute_actual_author_inference_and_verify_exact_preupdate_residual(self):
        # All input matrices and random initial weights here are TOYS, not paper data.
        torch.manual_seed(35)
        p=types.SimpleNamespace(
            r_dim=4,input_dim=4,r2_dim=3,r3_dim=2,mix_dim=2,mix_dim_2=2,
            hyper_hid_dim=5,hyper_hid_dim_2=5,thres=0.73,
            lr_r=0.15,lmda_r=0.001,lr_r2=0.001,lmda_r2=1e-6,
            lr_r3=0.001,lmda_r3=1e-5,temp_weight=2.5,
            alpha=0.75,max_iter=3,tol=0.0,
        )
        actual=module.DynPredNet(p,torch.device("cpu"))
        prev=torch.tensor([[0.3,0.4,0.1,0.8],[0.9,0.1,0.2,0.5]])
        x=torch.tensor([[0.8,0.1,0.5,0.2],[0.2,0.4,0.9,0.7]])
        rh_pre=torch.zeros((2,3),requires_grad=True)
        prior_rh=rh_pre.clone().detach()
        lower_post,rh_post,orig_error=actual.inf(x,prev,rh_pre)
        expected=torch.pow(
            lower_post-actual.temporal_prediction_one_(prev,prior_rh).clone().detach(),
            2
        ).view(2,-1).sum(1)
        self.assertEqual(tuple(orig_error.shape),(2,))
        self.assertTrue(torch.allclose(orig_error,expected,rtol=1e-6,atol=1e-6))
        # Compare to spatial reconstruction error: the source implementation
        # explicitly does NOT use pixel error as the three-level gate.
        spatial=torch.pow(x-actual.spatial_decoder(lower_post),2).sum(1)
        self.assertFalse(torch.allclose(orig_error,spatial,rtol=1e-4,atol=1e-4))
        low=(orig_error.min().item()-1e-4)
        high=(orig_error.max().item()+1e-4)
        self.assertTrue(bool(torch.all(orig_error>low)))
        self.assertFalse(bool(torch.any(orig_error>high)))
        # Control threshold 0.73: compare author-compatible predicate with
        # fixed config but do not pretend this toy yields published events.
        self.assertTrue(torch.equal(orig_error>p.thres,expected>0.73))
        print("AUTHOR_NUMERIC_GATE_LOSSES_TOY="+repr(orig_error.detach().tolist()))
        print("SECONDARY_PINNED_ACTUAL_INF_EXECUTED=TRUE")
if __name__=="__main__":
    unittest.main(verbosity=2)

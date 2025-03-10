--@funsearch.evolve
theorem mathd_algebra_393 (σ : Equiv ℝ ℝ) (h₀ : ∀ x, σ.1 x = 4 * x ^ 3 + 1) : σ.2 33 = 2 := by
  simp_all only [Equiv.toFun_as_coe, Equiv.invFun_as_coe]
  rw [σ.symm_apply_eq]
  simp_all only
  norm_cast

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

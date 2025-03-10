--@funsearch.evolve
theorem mathd_algebra_451 (σ : Equiv ℝ ℝ) (h₀ : σ.2 (-15) = 0) (h₁ : σ.2 0 = 3) (h₂ : σ.2 3 = 9)
    (h₃ : σ.2 9 = 20) : σ.1 (σ.1 9) = 0 := by
  simp only [Equiv.invFun_as_coe, eq_comm] at h₀ h₁ h₂ h₃
  simp only [Equiv.toFun_as_coe]
  rw [← Equiv.apply_eq_iff_eq_symm_apply σ] at h₂
  rw [← Equiv.apply_eq_iff_eq_symm_apply σ] at h₁
  have h₄ := (Equiv.apply_eq_iff_eq σ).mpr h₂
  rw [h₁] at h₄
  exact h₄

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

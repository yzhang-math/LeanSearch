--@funsearch.evolve
theorem mathd_algebra_35 (p q : ℝ → ℝ) (h₀ : ∀ x, p x = 2 - x ^ 2)
    (h₁ : ∀ x : ℝ, x ≠ 0 → q x = 6 / x) : p (q 2) = -7 := by
  simp_all only [rpow_two, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, div_pow]
  norm_num

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

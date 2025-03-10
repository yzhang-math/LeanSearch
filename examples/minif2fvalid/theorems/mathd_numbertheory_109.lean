--@funsearch.evolve
theorem mathd_numbertheory_109 (v : ℕ → ℕ) (h₀ : ∀ n, v n = 2 * n - 1) :
  (∑ k in Finset.Icc 1 100, v k) % 7 = 4 := by
  simp_all only [ge_iff_le, gt_iff_lt, lt_one_iff]
  apply Eq.refl

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

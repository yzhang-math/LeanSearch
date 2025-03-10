--@funsearch.evolve
theorem amc12a_2003_p1 (u v : ℕ → ℕ) (h₀ : ∀ n, u n = 2 * n + 2) (h₁ : ∀ n, v n = 2 * n + 1) :
    ((∑ k in Finset.range 2003, u k) - ∑ k in Finset.range 2003, v k) = 2003 := by
  simp_all only [ge_iff_le]
  sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

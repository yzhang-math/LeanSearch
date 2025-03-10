--@funsearch.evolve
theorem mathd_numbertheory_136 (n : ℕ) (h₀ : 123 * n + 17 = 39500) : n = 321 := by
  simp_all only [succ.injEq]
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

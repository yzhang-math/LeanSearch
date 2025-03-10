--@funsearch.evolve
theorem mathd_numbertheory_48 (b : ℕ) (h₀ : 0 < b) (h₁ : 3 * b ^ 2 + 2 * b + 1 = 57) : b = 4 := by
  simp_all only [succ.injEq]
  apply le_antisymm
  · nlinarith
  · nlinarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

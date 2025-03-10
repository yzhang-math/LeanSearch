--@funsearch.evolve
theorem mathd_numbertheory_335 (n : ℕ) (h₀ : n % 7 = 5) : 5 * n % 7 = 4 := by
  rw [Nat.mul_mod, h₀]

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

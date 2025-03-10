--@funsearch.evolve
theorem aime_1984_p1
  (u : ℕ → ℚ)
  (h₀ : ∀ n, u (n + 1) = u n + 1)
  (h₁ : ∑ k in Finset.range 98, u k.succ = 137) :
  ∑ k in Finset.range 49, u (2 * k.succ) = 93 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

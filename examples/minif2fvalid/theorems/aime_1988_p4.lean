--@funsearch.evolve
theorem aime_1988_p4 (n : ℕ) (a : ℕ → ℝ) (h₀ : ∀ n, abs (a n) < 1)
  (h₁ : (∑ k in Finset.range n, abs (a k)) = 19 + abs (∑ k in Finset.range n, a k)) : 20 ≤ n := by
  sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

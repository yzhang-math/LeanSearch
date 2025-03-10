--@funsearch.evolve
theorem mathd_algebra_15 (s : ℕ → ℕ → ℕ)
    (h₀ : ∀ a b, 0 < a ∧ 0 < b → s a b = a ^ (b : ℕ) + b ^ (a : ℕ)) : s 2 6 = 100 := by
  simp_all only [and_imp, zero_lt_two, zero_lt_succ]
  apply Eq.refl

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

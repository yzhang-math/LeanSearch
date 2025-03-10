--@funsearch.evolve
theorem amc12_2001_p9 (f : ℝ → ℝ) (h₀ : ∀ x > 0, ∀ y > 0, f (x * y) = f x / y) (h₁ : f 500 = 3) :
    f 600 = 5 / 2 := by
  specialize h₀ 500 _ (6 / 5) _
  · linarith
  · linarith
  calc
    f 600 = f (500 * (6 / 5)) := by
      congr
      norm_num
    _ = f 500 / (6 / 5) := by rw [h₀]
    _ = 3 / (6 / 5) := by rw [h₁]
    _ = 5 / 2 := by norm_num

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry

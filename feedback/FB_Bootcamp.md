M1:
-- Section 02 is called edge-detection, but thresholding is actually not a form of edge detection right?

M2:
-- General questions regarding the gaze concept. It seems to me that deepgaze assumes that you can see the whole scene and that it then predicts where you are likely to look.
However, prosthesis users don't see the full scene, they only see the part that the prosthesis focuses on. Does the concept of gaze then even still apply?
-- Also, what happens if the gaze prediction and the actual gaze do not align? The movement of the scenery gets messed up in the patients brain, won't it?

-- It says two reasons, then states 3.

-- The page contains several questions that can not be known by the reader, the information is only given in the answer. It doesn't really make sense that those answers are hidden, because it can not be used as kind of 'self-test' if you understand the material.

-- In 05: "Pick one (x, y) point from that map at random - bright spots are more likely." <- I assume it uses the probability of the map no?

-- In 06: The axes say in ms, in radians, in pixels, but then there is not axis. So the specification of the unit doesn't really make sense.

M3:

-- Intro: Higher frequency is not necessarily higher firing rate

-- In the shannon limit calculation, charge per phase is in uC. The current description says nC, and therefore the calculations are all wrong. 
-- The text in the 5 pulse parameters give me very much ai-generated vibe. It states obvious facts multiple times (Charge per pulse = amplitude x pulse width. Longer pulses deposit more charge at the same amplitude ), but then mentions certain things that will not at all be known to the participants (strenght-duration trade-off, refractory limits).
I think this text could do with more in-depth explanation of the concepts.

-- It breaks my heart a bit to say that the 5 parameters determine the complete stimulation given my background in 'non-conventional' stimulation (asymmetric pulses, non-rectangular shapes, etc.). Inter-train-interval is clearly also a parameter (which is later also used in the simulator).

-- 03: "A real cortical prosthesis drives ~100 electrodes at once.", of course, this is making a lot of assumptions on the system design. Should generalize more and state that this is an example.
-- Middle column with stim config is very small.

-- Stimulation panel needs more explanations. Power calculation based on fixed impedance is not very realistic, would be better to use fixed voltage. Or current limit (I've never seen people using power limits in stim).
-- can we stop the panel (and maybe remove the timer) when the stimulator is in idle state?
-- Clicking surprise me automatiically starts the stimulator, which is not very intuitive. 
-- Because the code uses iti instead of train repetition rate, for trains with different lengths stimulating multiple trains brings them out of sync. 


-- k = log10(Q) + log10(Qd) drops by 2 × log10(2) ≈ 0.60. Should be log10(0.5). But we ask about the charge per phase. This calculation is not the charge per phase but the shannon factor.

-- The answer to Q2 suddenly gives information that is never presented before (and might also be too simplified..).

-- The answer to Q3 doesn't make sense (and the question perhaps also not). I think the content should be more comprehensive and the questions more specific.

-- Q4 doesn't give all information needed to calculate the answer. The area of the electrode is not given.


M4:
-- Misses introduction of a lot of things (dynaphos itself most importantly) such as the different parameters used in 01.

-- "Slide eccentricity from 0.5 to 14." > the range of the slider is 0.5-7.5.

-- "Set N = 200. What is the smallest feature you could read?" Both the question and the answer are not clear to me.

-- Of course there are also physical/technological limitations to the electrode placement, which should be addressed.

--"Drop peak current to ~25 µA. What breaks first - shape or brightness?", to me it seems that the threshold is more around 35-40uA. Below that I don't see any phosphene.

-- "Compare "real" vs "disable trace" - which is biologically correct?" This seems a bit of a rethorical question given the name "real"...

-- The questions and concepts in 04 need much more background. Even I, after 4 years working on a visual prosthesis, don't understand the terms used (like activation delay), and their explanation.

I'd sort folders by status instead:

videos/
  <slug>/              ← currently in production (only 1–3 here)
  _arsip/<slug>/       ← finished/uploaded (the _ hides it from `claude-video` list)
  _lab/motion-lab/     ← experiments, not for upload
hasil/
  <slug>/              ← final, NOT uploaded yet = your upload queue
  _tayang/<slug>/      ← uploaded (move it here after posting)
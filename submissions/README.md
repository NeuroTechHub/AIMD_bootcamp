# Submit your solutions

This folder is where teams submit their bootcamp solutions. One subfolder per team,
contributed via a pull request from a fork.

## How to submit

1. **Fork** this repository on GitHub (`NeuroTechHub/AIMD_bootcamp`).
2. In your fork, **create a branch** named after your team:
   ```
   git checkout -b team-<your-team-name>
   ```
3. Inside `submissions/`, **add a folder with your team name** and drop your solutions in it:
   ```
   submissions/
   └── <your-team-name>/
       ├── README.md          # short description of your approach
       ├── M1-...             # whichever modules you worked on
       └── ...
   ```
4. Commit and push the branch to your fork, then **open a pull request** against
   the `submissions` branch of this repo.

## Conventions

- Folder name: lowercase, hyphens for spaces (e.g. `team-neurolight`, `phosphene-hackers`).
- Keep submissions self-contained — anything needed to read or rerun your work lives
  in your team folder.
- Don't modify files outside `submissions/<your-team-name>/`.
- Large binaries: prefer a link over committing the file.

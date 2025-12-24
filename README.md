# cloudsecuritytool

## Running Locally

Make sure you are in the repo root, then run:

```bash
npm install
npm run dev
```

## Publishing this repository to GitHub

If you do not see these files on your GitHub repository yet, push the current working copy to your own remote:

1. Create a new empty GitHub repository (without initializing it with a README).
2. Add it as a remote in this workspace:
   ```bash
   git remote add origin git@github.com:<your-username>/<your-repo>.git
   ```
3. Verify the branch you want to publish (this workspace uses `main` by default):
   ```bash
   git branch --show-current
   ```
4. Push everything to GitHub:
   ```bash
   git push -u origin main
   ```
   If your current branch has a different name, replace `main` accordingly.
5. After the push completes, refresh the GitHub page for your repository—the files from this workspace will now appear in that branch.

If Git prompts for authentication, use an SSH key or a GitHub personal access token as appropriate for your account.

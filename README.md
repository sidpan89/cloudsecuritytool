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

### If you prefer to use the GitHub UI (no commands)
This environment cannot push to your GitHub account automatically. To publish without running any commands locally:

1. On GitHub, create a new empty repository (set the default branch to `main` to match this workspace).
2. Open the repository and choose **Add file → Upload files**.
3. Drag the entire project folder from your machine into the upload area (GitHub supports folder uploads). Wait for the file list to finish rendering.
4. Enter a commit message and click **Commit changes**. Your files will now be on the `main` branch of the new repository.

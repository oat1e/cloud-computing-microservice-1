# gcloud init Step-by-Step Guide

## Current Step: Configuration Selection

**Choose option 1** to re-initialize your existing configuration.

```
Please enter your numeric choice: 1
```

## What Happens Next:

### Step 1: Login (if needed)
You'll be asked to log in. It will open a browser window:
```
You must log in to continue. Would you like to log in (Y/n)? Y
```
- Click "Allow" in the browser
- You're already logged in as `hhz2102@columbia.edu`, so this might skip

### Step 2: Project Selection
You'll see a list of projects:
```
Pick cloud project to use:
 [1] your-project-id-1
 [2] your-project-id-2
 [3] Create a new project
Please enter numeric choice or text value (must contain at least one number):
```

**Options:**
- **If you see your project**: Enter its number
- **If you need to create one**: Enter `3` or type "Create a new project"
  - You'll be asked for a project name
  - Project ID will be auto-generated (or you can specify)

### Step 3: Default Region
You'll be asked to set a default region:
```
Do you want to configure a default Compute Region and Zone? (Y/n)? Y
```
- Enter `Y`
- Select a region (e.g., `us-central1`)

## Quick Commands After Init

Once `gcloud init` completes, verify your setup:

```bash
# Check current project
gcloud config get-value project

# List all projects (if you need to switch)
gcloud projects list

# Set a specific project (if needed)
gcloud config set project YOUR_PROJECT_ID
```

## If You Need to Create a Project

If you don't have a project yet, you can create one:

**Option A: During gcloud init**
- Select option 3 "Create a new project"
- Follow the prompts

**Option B: Via command line (after init)**
```bash
gcloud projects create matcha-api-project --name="Matcha API Project"
gcloud config set project matcha-api-project
```

**Option C: Via Web Console**
- Go to https://console.cloud.google.com
- Click "Select a project" → "New Project"
- Create project, then run `gcloud config set project YOUR_PROJECT_ID`

## After gcloud init Completes

You're ready to proceed with the deployment steps in `README_DEPLOYMENT.md`!


# Contribution Guide

Thank you for considering contributing to the Technique Research Report (TRR)
repository. The amount of work it takes to research hundreds of attack
techniques across numerous platforms can be overwhelming, but teamwork will
accelerate the pace at which we can chip away at the problem. For more
information on this initiative's goal, please see the [Project Overview]
documentation.

Please take a moment to review this document before submitting a pull request.
Following these guidelines helps to communicate that you respect the time of the
repository maintainers. In return, they should reciprocate that respect in
addressing your issue, assessing changes, and helping you finalize your pull
requests.

## Getting Started

Contributing to the repository follows the [GitHub Flow] strategy. To summarize
what this means in practice, a contributor must complete the following steps:

1. TRR scoping
2. Create a branch
3. Write the TRR
4. Create a pull request
5. Address review comments
6. Merge the pull request
7. Delete your branch locally

### TRR scoping

The first task is determining the scope of the new TRR. Generally, a TRR should
cover a single attack technique for one platform. It may cover all platforms
where the technique is functionally similar (for example, macOS and Linux share
some identical techniques due to their both being Unix derivatives). We leave it
to the author's discretion as to whether it is best to combine or separate
platforms, as a rule of thumb you should separate them when very little content
is relevant to both and combine if there are large portions that apply to both.
Using a whimsical example, a TRR might cover "X001.001 Eating It" for both the
Cakes and Pies platforms because the steps are very similar for both. But there
would be separate TRRs for Cakes and Pies for "X001.002 Baking It" because the
technique is functionally very different for each.

Unlike traditional frameworks such as MITRE ATT&CK or the Azure Threat Research
Matrix (ATRM), the TRR repository is designed to be independent of any external
classification system. Instead, each documented technique is assigned a unique
TRR ID to ensure that research remains flexible and is not limited by predefined
frameworks. If a technique does map to existing frameworks, those mappings are
included in the metadata for reference but they are not a requirement for a
technique to be documented, nor does a TRR have to adhere to the scope defined
in other frameworks.

> [!TIP]
> We are unlikely to accept TRRs for a technique under the "Execution" tactic.
> You can read our reasoning at [Mistaken Identification: When an Attack
> Technique isn't a Technique]. We'll probably ask you to re-scope the TRR to
> whatever technique it's actually discussing.

### Create a branch

#### Branch naming

Each branch must contain a single TRR and should be named according to the
technique it addresses, with a "report/" prefix. For example, if a contributor
wanted to research the "DCSync" technique, they would create a branch named
`report/dcsync` where they would stage all their work. Please use all lowercase
letters and underscores instead of spaces in branch names.

Every new branch must be based on the latest commit in the `main` branch to
ensure it has the most recent version.

#### Repo folder structure

The repo uses the following organizational structure:

```text
root
\_reports
  \_trr_id
    \_platform
      |_images
      |_ddms
      |_README.md  (this is the main TRR markdown)
      |_metadata.json (machine-readable metadata for indexing)
```

Each TRR will be in its own folder under the 'reports' folder, with an `images`
and `ddms` subfolder to hold the images and Detection Data Models (DDMs) used in
the TRR. TRR IDs are assigned incrementally when the TRR is merged into the main
branch, so draft TRRs should use "trr0000" as a placeholder (this will be
automatically replaced with the new ID when the TRR is accepted). The TRR will
be written in Markdown and will be named "README.md" (this causes GitHub to load
it automatically when displaying the folder). A separate metadata JSON file will
accompany the TRR to facilitate indexing and searching.

The name of the platform folder should use the abbreviation defined in the
`platforms.json` file in the root of the repository. This contains a JSON list
of key/value pairs where the key is the platform's assigned abbreviation and the
value is the full (human readable) platform name. For example, Azure has been
assigned the abbreviation of `azr`, so a TRR for Azure would be placed in the
folder `/reports/trr0000/azr/`.

There is a [template folder] available that you can use to set up the proper
folder structure and files for a new TRR. Simply create a new branch and copy
the template folder into the /reports/ folder in your branch. This sets up the
folders and files needed to write and submit a new TRR.

#### Handling Techniques that Cover Multiple Platforms

If a TRR covers a technique that applies to multiple platforms (for example, a
technique that works identically on macOS and Linux), list both platforms in the
metadata section and JSON file. Select the platform that seems the most relevant
and place the TRR in a folder with the corresponding abbreviation. The
`platforms` section of the metadata must list this platform first. This allows
readers to find the TRR via the index or the frontend search using either
platform.

For example, a TRR on the technique of stealing credentials from the NTDS.dit
file on a Windows domain controller could be stored in a folder named 'win' (for
Windows) or 'ad' (for Active Directory), because the technique applies to both
platforms. The author can select whichever platform seems the best match as the
primary platform. If the author selected "Windows" (because the techniques
addressed were abusing Windows features, for example), they would place the TRR
in the folder `/reports/trr0000/win` and list the platforms as "Windows, Active
Directory."

### Write the TRR

Writing a TRR is not easy, it requires a lot of technical expertise. Before you
begin, please read up on the [strategy] that informs this process, [how to do
technique analysis and modeling], and read through a few of the existing TRRs to
get a sense of what we're expecting.

Once you're ready to begin researching and writing, there is a [TRR Guide] with
details on the sections that must be included, a [template], a [style guide], an
[FAQ], and an [example TRR].  

> [!TIP]
> If an existing TRR already has a really good explanation of a concept
> that applies to your technique, you should just use it and add to it. There is
> no need to rewrite what has already been written well. Just add whoever wrote
> it as a contributor to the new TRR, to give them credit for their excellent
> explanation.

### Create a pull request

When your TRR is completed, create a new pull request (PR) for your branch. Use
the technique name for the name of your PR. This will trigger the process for
reviewing your TRR for inclusion in the repo.

### Address review comments

Reviewers will leave comments or suggest changes. You should address all
comments and make the requested changes. GitHub provides the platform to have a
conversation between the author and various reviewers, so we can all come to
agreement on how to make the best TRR that we can collectively create.

### Merge the pull request

Once the required approvals have been obtained, the TRR is ready for inclusion!
The repo maintainers will assign a TRR ID and merge it into the `main` branch.
Congratulations and thank you for contributing!

### Delete your branch locally

The remote branch will be deleted automatically when it is merged, but you might
want to clean up your local repo by deleted merged branches.

## Adding to an Existing TRR

If you have something to add to a TRR that has already been accepted into the
repo, you should clone the main branch and then create a new branch to track
your updates. Name the new branch using the TRR ID and add "update" (for
example, "trr0018_update"). When you've completed your updates, push your
changes and create a pull request (again, adding "Update" to the name).

[Project Overview]: ./PROJECT-OVERVIEW.md
[GitHub Flow]: https://docs.github.com/en/get-started/using-github/github-flow
[TRR Guide]: TECHNIQUE-RESEARCH-REPORT.md
[template]: ./examples/trr0000/platform_abbr/README.md
[template folder]: ./examples/trr0000
[style guide]: STYLE-GUIDE.md
[example TRR]: ./examples/trr0001/phy/README.md
[Mistaken Identification: When an Attack Technique isn't a Technique]:
    https://medium.com/p/8cd9dae6e390
 [strategy]: https://medium.com/@vanvleet/threat-detection-strategy-a-visual-model-b8f4fa518441
 [how to do technique analysis and modeling]: http://needlink
 [FAQ]: FAQ.md

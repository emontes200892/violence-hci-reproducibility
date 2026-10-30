# Publishing a version and obtaining an optional DOI

## GitHub release

1. Run `python scripts/reproduce.py --verify` and review the generated tables.
2. Review the README's data-availability scope against what the manuscript claims.
3. Push the reviewed repository to GitHub and wait for the reproduction workflow.
4. Tag the reviewed commit `v0.1.0` and create the corresponding release.
5. Cite the repository URL and exact version in the production response only after
   publication succeeds. A ZIP prepared locally is not a published GitHub repository.

This initial release can support the numerical analyses, but does not contain the
complete article-level corpus list, full anonymized questionnaire or video.
Resolve these advertised supplements before claiming that all supplementary
materials are available in this release.

## What a DOI adds

GitHub records code history and hosts ongoing development. A DOI identifies a
specific archived research object. Zenodo can archive a public GitHub release and
assign its own DOI, preserving the exact version cited by a paper.

An archive DOI is optional for creating this repository. The DOI of the article
and any later DOI of the repository are separate identifiers. Do not invent a DOI
or insert one into `CITATION.cff` before Zenodo has issued it.

After linking GitHub and Zenodo, enable this repository in Zenodo and create a
versioned GitHub release. Review the resulting Zenodo record and its DOI before
updating the citation metadata and manuscript repository reference. Enabling a
Zenodo integration is a separate account-authorization action.

Official instructions:
- https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content
- https://help.zenodo.org/docs/github/archive-software/

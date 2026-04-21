# Deployment

<!-- last_review: 2026-04-21 -->

## Environment variables

If there are new or changed environment variables, a dxw-er will need to run:
`dalmatian service set-environment-variable -i caselaw-stg -e staging -s public -k NEW_ENV_VAR -v VALUE`
(possibly with `caselaw` and `prod` for production and `editor` for the editor ui)

## Staging

The `main` branch is automatically deployed with each commit. The deployed app can be viewed at [https://staging.caselaw.nationalarchives.gov.uk/](https://staging.caselaw.nationalarchives.gov.uk/)

## Production

To deploy to production:

1. Follow the [release process](RELEASE.md) to create a new release.
1. Automated workflow will then force-push that release to the `production` branch, which will then be deployed to the production environment.
1. If you need to roll back to an earlier version, force-push that version to `production` manually. Explictly run `dalmatian service deploy` (with the right `-i`, `-e`, `-s` flags) if it is not a new commit.

The production app is at [https://caselaw.nationalarchives.gov.uk/](https://caselaw.nationalarchives.gov.uk/)

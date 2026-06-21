# Backlog After Stage 2

Stage 2 local added upload support, richer report fields, deterministic scenarios, and stronger validation. The items below remain planned improvements.

## Richer Risk Report

Why it matters:

Stage 2 added a richer report structure. The next step is to make the report more configurable and easier to export.

Rough complexity:

Medium.

What not to overclaim:

Do not call it a full risk system. It would still be a report layer over simplified metrics.

## Stronger Schemas

Why it matters:

Stage 2 added stronger response models. The next step is structured error response models and stricter request validation for optional parameters.

Rough complexity:

Medium.

What not to overclaim:

Schema validation improves input quality, but it does not guarantee correct portfolio economics.

## Multipart CSV Upload

Why it matters:

Implemented in Stage 2 for summary and report endpoints. The next step is better upload metadata and size/content safeguards.

Rough complexity:

Medium.

What not to overclaim:

File upload is usability work, not a new risk methodology.

## Scenario Engine

Why it matters:

Stage 2 added deterministic built-in shocks. User-defined shocks are more useful than hardcoded scenarios.

Rough complexity:

Medium to high.

What not to overclaim:

Scenario results are assumptions, not forecasts.

## Better Error Responses

Why it matters:

Structured errors help API consumers debug bad input data faster.

Rough complexity:

Low to medium.

What not to overclaim:

Cleaner errors do not solve bad upstream data.

## Data Adapters

Why it matters:

Adapters can make the same risk backend work with different market data sources.

Rough complexity:

Medium to high.

What not to overclaim:

Do not claim full market-agnostic support until adapters are actually implemented and tested.

## Optional Dashboard Later

Why it matters:

A small dashboard can make the API easier to demo.

Rough complexity:

Medium.

What not to overclaim:

The dashboard should be a view into the API, not the core product.

## Hosted API Demo Later

Why it matters:

A hosted demo makes the project easier to review.

Rough complexity:

Medium.

What not to overclaim:

Hosted sample data is still sample data. It should not be presented as live market risk output.

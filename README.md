**Overview:**
During GCP Organization/Project onboarding, Prisma Cloud uses a service account to make authorized API calls to GCP. As per the current design, when Prisma Cloud makes GCP API calls and these calls eat up the API rate limit quota of the GCP project where the service account is created. 
So for deployments where customers have onboarded multiple GCP Organizations/Projects of any size in Prisma Cloud with a single service account, all the API calls made from Prisma Cloud to these multiple GCP Organizations/Projects consume the same rate limit quota. This causes rate limit exceptions due to which resources metadata are not ingested and that leads to lack of visibility for customers.


**Solution:**
With the new approach, we intend to solve this problem by delegating the rate limit quota from the service account project to the target project that’s onboarded in Prisma Cloud. GCP provides an option to specify the project from which the rate quota will be consumed. This would mean that the APIs calls from Prisma Cloud would consume quota from the respective onboarded GCP Projects.

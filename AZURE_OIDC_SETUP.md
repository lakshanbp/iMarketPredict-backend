# Azure Federated Identity Credentials Setup for GitHub Actions

This document provides step-by-step instructions for configuring Azure Active Directory federated identity credentials to enable OpenID Connect (OIDC) authentication for GitHub Actions workflows.

## Overview

The GitHub Actions workflow has been updated to use OIDC authentication with Azure, which is more secure than using client secrets. This requires setting up federated identity credentials in Azure Active Directory.

## Prerequisites

- Azure subscription with appropriate permissions
- Access to Azure Active Directory
- GitHub repository with Actions enabled
- Azure App Service (iMarketPredict) already created

## Setup Instructions

### 1. Register Azure Application (if not already done)

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Find or create the `iMarketPredict` application

### 2. Configure Federated Identity Credentials

1. In your Azure AD application (`iMarketPredict`), go to **Certificates & secrets**
2. Click on the **Federated credentials** tab
3. Click **Add credential**
4. Choose **GitHub Actions deploying Azure resources** as the scenario
5. Fill in the details:
   - **Organization**: `lakshanbp`
   - **Repository**: `iMarketPredict-backend`
   - **Entity type**: Branch
   - **GitHub branch name**: `main`
   - **Name**: `iMarketPredict-main-branch`
   - **Description**: `Federated credential for main branch deployment`

### 3. Note Required Values

After setting up the federated credentials, you'll need these values for GitHub secrets:

- **Client ID**: Found in the app registration overview page
- **Tenant ID**: Found in the app registration overview page  
- **Subscription ID**: Your Azure subscription ID

### 4. Configure GitHub Secrets

In your GitHub repository settings, add these secrets:

- `AZUREAPPSERVICE_CLIENTID`: The Application (client) ID from Azure AD
- `AZUREAPPSERVICE_TENANTID`: The Directory (tenant) ID from Azure AD
- `AZUREAPPSERVICE_SUBSCRIPTIONID`: Your Azure subscription ID

**Note**: You no longer need `AZUREAPPSERVICE_CLIENTSECRET` with OIDC authentication.

### 5. Assign Azure Permissions

Ensure the service principal has the necessary permissions:

1. Go to your **Azure App Service** (iMarketPredict)
2. Navigate to **Access control (IAM)**
3. Add role assignment for the service principal:
   - **Role**: `Website Contributor` or `Contributor`
   - **Assign access to**: User, group, or service principal
   - **Select**: Your `iMarketPredict` application

## Verification

After completing the setup:

1. Push changes to the `main` branch
2. Check the GitHub Actions workflow run
3. The Azure login step should now succeed without client secret errors

## Troubleshooting

### Common Issues

1. **"No matching federated identity record found"**
   - Verify the organization, repository, and branch names are correct
   - Ensure the entity type matches (Branch vs Environment vs Pull Request)

2. **"Permission denied"**
   - Check that the service principal has appropriate permissions on the Azure resources
   - Verify the subscription ID is correct

3. **"Invalid audience"**
   - Ensure you selected "GitHub Actions deploying Azure resources" as the scenario
   - The audience should be set to `api://AzureADTokenExchange`

## Security Benefits

Using federated identity credentials provides several security advantages:

- **No secrets in GitHub**: No need to store and rotate client secrets
- **Short-lived tokens**: Tokens are automatically issued and expire quickly
- **Scoped access**: Credentials are tied to specific repositories and branches
- **Audit trail**: Better visibility into authentication events

## Additional Resources

- [Azure OIDC Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation)
- [GitHub Actions Azure Login](https://github.com/marketplace/actions/azure-login)
- [Azure App Service Deploy Action](https://github.com/marketplace/actions/azure-webapp)
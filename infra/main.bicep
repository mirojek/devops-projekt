@description('Nazwa rejestru kontenerów ACR (musi być globalnie unikalna, tylko małe litery i cyfry)')
param acrName string

@description('Lokalizacja zasobów (np. westeurope)')
param location string = resourceGroup().location

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

# HubSpot MCP Server

Serveur MCP (Model Context Protocol) pour l'API HubSpot CRM.

## Installation

```bash
npm install
npm run build
```

## Configuration

Définir une des variables d'environnement suivantes:

### Option 1: Private App Token (Recommandé)
```bash
export HUBSPOT_ACCESS_TOKEN="pat-xxx-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Option 2: API Key (Legacy)
```bash
export HUBSPOT_API_KEY="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

## Création d'une Private App HubSpot

1. Aller sur **HubSpot Settings → Integrations → Private Apps**
2. Cliquer sur **Create a private app**
3. Donner un nom à l'app
4. Dans l'onglet **Scopes**, sélectionner:
   - `crm.objects.contacts.read` / `write`
   - `crm.objects.companies.read` / `write`
   - `crm.objects.deals.read` / `write`
   - `crm.objects.tickets.read` / `write`
   - `crm.schemas.contacts.read`
   - `crm.schemas.companies.read`
   - `crm.schemas.deals.read`
5. Créer l'app et copier le token généré

## Configuration Claude Desktop

Ajouter dans `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hubspot": {
      "command": "node",
      "args": ["/chemin/vers/hubspot-mcp/build/index.js"],
      "env": {
        "HUBSPOT_ACCESS_TOKEN": "pat-xxx-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      }
    }
  }
}
```

## Outils Disponibles (48 outils)

### Contacts (6 outils)
- `list_contacts` - Lister les contacts
- `get_contact` - Obtenir un contact par ID/email
- `create_contact` - Créer un contact
- `update_contact` - Mettre à jour un contact
- `delete_contact` - Archiver un contact
- `search_contacts` - Rechercher des contacts

### Companies (6 outils)
- `list_companies` - Lister les entreprises
- `get_company` - Obtenir une entreprise
- `create_company` - Créer une entreprise
- `update_company` - Mettre à jour
- `delete_company` - Archiver
- `search_companies` - Rechercher

### Deals (6 outils)
- `list_deals` - Lister les opportunités
- `get_deal` - Obtenir un deal
- `create_deal` - Créer un deal
- `update_deal` - Mettre à jour
- `delete_deal` - Archiver
- `search_deals` - Rechercher

### Tickets (6 outils)
- `list_tickets` - Lister les tickets
- `get_ticket` - Obtenir un ticket
- `create_ticket` - Créer un ticket
- `update_ticket` - Mettre à jour
- `delete_ticket` - Archiver
- `search_tickets` - Rechercher

### Pipelines (2 outils)
- `list_pipelines` - Lister les pipelines
- `get_pipeline` - Obtenir un pipeline

### Associations (3 outils)
- `get_associations` - Obtenir les associations
- `create_association` - Créer une association
- `delete_association` - Supprimer une association

### Properties (2 outils)
- `list_properties` - Lister les propriétés
- `get_property` - Obtenir une propriété

### Owners (2 outils)
- `list_owners` - Lister les propriétaires
- `get_owner` - Obtenir un propriétaire

### Engagements (9 outils)
- `list_notes` / `create_note` - Notes
- `list_tasks` / `create_task` - Tâches
- `list_calls` / `create_call` - Appels
- `list_emails` - Emails
- `list_meetings` / `create_meeting` - Réunions

### Batch Operations (4 outils)
- `batch_create` - Créer en masse
- `batch_read` - Lire en masse
- `batch_update` - Mettre à jour en masse
- `batch_archive` - Archiver en masse

## Exemples d'utilisation

### Lister les contacts
```
list_contacts avec limit: 10, properties: ["email", "firstname", "lastname"]
```

### Créer un contact
```
create_contact avec email: "john@example.com", firstname: "John", lastname: "Doe"
```

### Rechercher des deals
```
search_deals avec filterGroups: [{ filters: [{ propertyName: "amount", operator: "GT", value: "10000" }] }]
```

### Créer une association contact → company
```
create_association avec fromObjectType: "contacts", fromObjectId: "123", toObjectType: "companies", toObjectId: "456"
```

## Ressources

| URI | Description |
|-----|-------------|
| `hubspot://contacts` | Liste des contacts |
| `hubspot://companies` | Liste des entreprises |
| `hubspot://deals` | Liste des deals |
| `hubspot://tickets` | Liste des tickets |

## Licence

MIT

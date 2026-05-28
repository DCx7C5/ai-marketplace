# Salesforce Data Dictionary

A Model Context Protocol (MCP) server for describing and managing Salesforce objects. This MCP provides tools for listing, describing, and creating data dictionaries from Salesforce objects, making it easy to explore and document your Salesforce schema.

## Features

- **Describe Salesforce Objects**: Get detailed field information for any Salesforce object
- **List All Objects**: Browse all available Salesforce objects
- **Find Similar Objects**: Search for objects with similar names
- **CSV/Excel Export**: Export field information; Excel export supports multiple objects (one sheet per object)
- **Data Dictionary Creation**: Convert Salesforce objects to data dictionaries
- **Smart Object Detection**: Automatically find similar objects if exact match not found

## Prerequisites

- **Salesforce CLI**: Must be installed and authenticated
- **Node.js**: Version 16 or higher
- **npm**: For package management

### Installing Salesforce CLI

```bash
npm install -g @salesforce/cli
sf login org
```

## Installation

You can run this MCP either locally from the repo (build then point Cursor to `dist/index.js`) or directly via `npx` without cloning.

### Option A: Use npx (recommended)

Add this to `~/.cursor/mcp_servers.json`:

```json
{
  "mcpServers": {
    "salesforce-data-dictionary": {
      "command": "npx",
      "args": ["-y", "salesforce-mcp"],
      "env": {}
    }
  }
}
```

- `npx -y salesforce-mcp` will fetch and run the latest published version.
- No local checkout required.

### Option B: Local checkout

1. Clone and build:
```bash
git clone <repository-url>
cd dataDicMCP
npm install
npm run build
```

2. Configure Cursor to run the built entrypoint:
```json
{
  "mcpServers": {
    "salesforce-data-dictionary": {
      "command": "node",
      "args": ["/Users/ffarath/Documents/projects/dataDicMCP/dist/index.js"],
      "env": {}
    }
  }
}
```

3. Restart Cursor.

## Available Tools

### 1. `Describe Salesforce Object`
Describe a Salesforce object and return its field information in CSV format.

**Parameters:**
- `objectName` (string): Name of the Salesforce object to describe (e.g., Account, Contact, CustomObject__c)
- `outputFile` (string, optional): Filename to save the CSV output (e.g., 'account_fields.csv')

**Example:**
```
Describe the Account object and save the results to account_fields.csv
```

### 2. `List Salesforce Objects`
List all available Salesforce objects.

**Parameters:**
- `searchTerm` (string, optional): Search term to filter objects

**Example:**
```
List all Salesforce objects that contain "user" in the name
```

### 3. `Find Similar Objects`
Find Salesforce objects with similar names.

**Parameters:**
- `searchTerm` (string): Search term to find similar object names

**Example:**
```
Find objects similar to "Account"
```

### 4. `Create Data Dictionary`
Create an Excel data dictionary from one or more Salesforce objects (one tab per object labeled with the object label).

**Parameters:**
- `objects` (string): Comma-separated list of Salesforce objects (e.g., "Account, Contact, Opportunity")
- `outputFile` (string): Excel filename (e.g., "data_dictionary.xlsx")

**Example:**
```
Create a data dictionary for Account, Contact, Opportunity and save to data_dictionary.xlsx
```

## Example Usage

### Describing a Salesforce Object

```
Describe the Account object and show me all its fields in CSV format
```

The MCP will:
1. List all Salesforce objects using `sf sobject list --sobject all`
2. Check if "Account" exists
3. If found, describe it using `sf sobject describe --sobject Account`
4. Parse the JSON response and display it as a user-friendly CSV

### Creating Excel Data Dictionary

```
Create a data dictionary from "Account, Contact, Opportunity" and save to sales_schema.xlsx
```

This will generate an Excel with three sheets named from each object's label.

## CSV/Excel Output Format

Columns included:
- Field Name
- Type
- Label
- Description
- Required
- Unique
- Length
- Precision
- Scale
- Default Value
- Picklist Values
- Reference To
- Relationship Name

## Error Handling

- **Object Not Found**: If the exact object name isn't found, it suggests similar objects
- **Salesforce CLI Errors**: Clear error messages for authentication or connection issues
- **Invalid Object Names**: Helpful suggestions for common naming patterns

## Salesforce CLI Integration

This MCP relies on the Salesforce CLI for all operations:

- `sf sobject list --sobject all`: Lists all available objects
- `sf sobject describe --sobject <ObjectName>`: Describes a specific object

Make sure you're authenticated with the correct Salesforce org:

```bash
sf login org
sf org list
```

## Supported Salesforce Objects

- Standard objects (Account, Contact, Lead, Opportunity, etc.)
- Custom objects (CustomObject__c)
- System objects
- External objects

## License

MIT License - see LICENSE file for details.

# MyEMSL Status Reporting Site

## Overview
This site will provide a conduit for lots of different types of researchers to determine the status of their data within the MyEMSL system. Division directors will probably want to see a different, higher level view of system operations, while an instrument operator will most likely care about the particular instrument(s) in their charge.

These views will likely include...

* Site-level overviews for EMSL Management
    - 30,000 ft view aggregated over classes like instrument type, facilities, researchers, proposals, etc.
    - Fewer details immediately visible, but still available
  
- Facility-level views for individual program managers and capability leads
    - Collections of instruments that can be personalized by user id or client-side cookie
    - More details available immediately, with breakdowns within a given instrument at the proposal and operator level
  
- Instrument-level views for custodians and operators
    - Details for a given instrument that include a date-selectable range of activity (i.e. what has happened on that
  instrument over a given period of time) that shows files uploaded and various metadata about those files
    - Lots of detail available, with extra detail on jobs that are still in progress for upload
  
- Some kind of different view for EMSL Users (external and internal) that is some mix of the above

The development version of the site will (eventually) be hosted at [http://wfdev30w.pnl.gov/myemsl_status](http://wfdev30w.pnl.gov/myemsl_status)

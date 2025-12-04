import React from "react";

export default function Overview({ items }){
  return (
    <div style={{padding:20}}>
      <h1>Overview — Recent MR Analyses</h1>
      {items && items.length ? items.map(it => (
        <div key={`${it.project_id}-${it.mr_iid}`} style={{border:"1px solid #ddd", padding:12, marginBottom:8}}>
          <div><strong>Project</strong>: {it.project_id} — <strong>MR</strong>: {it.mr_iid}</div>
          <div dangerouslySetInnerHTML={{__html: it.summary}} />
          <div style={{fontSize:12, color:"#666"}}>Processed: {String(it.processed)}</div>
        </div>
      )) : <div>No analyses yet.</div>}
    </div>
  );
}

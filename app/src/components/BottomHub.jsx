import React, { useEffect } from 'react'

export default function BottomHub() {
  useEffect(() => {
    // nothing required for now; CSS handles animations
  }, [])

  return (
    <div className="bottom-hub" aria-hidden>
      <div className="hub-inner">
        <svg viewBox="0 0 100 60" preserveAspectRatio="none" className="topo-svg">
          <line x1="20" y1="30" x2="60" y2="10" className="topo-link" />
          <line x1="60" y1="10" x2="80" y2="45" className="topo-link" />
          <line x1="80" y1="45" x2="20" y2="30" className="topo-link" />

          <circle cx="20" cy="30" r="3.5" className="topo-node node-a" />
          <circle cx="60" cy="10" r="3.5" className="topo-node node-b" />
          <circle cx="80" cy="45" r="3.5" className="topo-node node-c" />
        </svg>

        <div className="node-label node-a-label">Gateway</div>
        <div className="node-label node-b-label">Edge</div>
        <div className="node-label node-c-label">Client</div>

        <div className="packet-dot path-ab" />
        <div className="packet-dot path-bc" />
        <div className="packet-dot path-ca" />

      </div>
      <div className="hub-footer">
        <div className="stats-item">Peers: <strong id="hub-peers">{ /* dynamic if needed */ } 3</strong></div>
        <div className="stats-item">Traffic: <strong>●●●</strong></div>
      </div>
    </div>
  )
}

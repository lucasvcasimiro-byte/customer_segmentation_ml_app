/**
 * Overview.jsx  —  Executive Summary section
 *
 * Shows:
 *   • Hero headline with animated gradient text
 *   • Tech-stack pills
 *   • KPI metric cards
 *   • Overview donut chart (cluster distribution)
 *   • Written project summary
 */
import { useMemo } from 'react'
import KPICard from '../components/common/KPICard'
import SectionHeader from '../components/common/SectionHeader'
import InteractivePlot from '../components/common/InteractivePlot'
import { kpiData, clusters } from '../data/clusterData'

// Colour palette for the donut slices
const DONUT_COLORS = ['#2dd4bf', '#f43f5e', '#3b82f6', '#f59e0b', '#a78bfa', '#ec4899', '#06b6d4']

export default function Overview() {
  // Donut values and pulling configs for ALL customers
  const totalCustomers = 32571
  const donutValues = [6636, 11606, 2131, 5662, 1228, 3123, 2185]
  const donutPull = [0, 0.04, 0, 0, 0, 0, 0]

  // Build Plotly donut chart trace statically
  const donutTrace = useMemo(() => ({
    type:      'pie',
    hole:      0.52,
    labels:    clusters.map(c => c.name),
    values:    donutValues,
    marker:    { colors: DONUT_COLORS, line: { color: '#07091a', width: 3 } },
    textinfo:  'percent',
    hovertemplate: '<b>%{label}</b><br>Customers: %{value}<br>Share: %{percent}<extra></extra>',
    textfont:  { color: '#eef2ff', size: 12 },
    pull:      donutPull,
  }), [])

  const donutLayout = useMemo(() => ({
    showlegend: true,
    legend: {
      orientation: 'v',
      x: 1.05,
      y: 0.5,
    },
    annotations: [{
      text: `<b>${totalCustomers.toLocaleString()}</b><br>customers`,
      x: 0.5, y: 0.5,
      font: { size: 14, color: '#eef2ff', family: 'Space Grotesk' },
      showarrow: false,
    }],
    margin: { l: 20, r: 120, t: 20, b: 20 },
  }), [])

  // CSV download payload for the donut
  const donutCsv = useMemo(() => ({
    headers: ['Cluster', 'Name', 'Count', 'Percentage'],
    rows:    clusters.map((c, idx) => {
      const val = donutValues[idx]
      const pct = ((val / totalCustomers) * 100).toFixed(1)
      return [c.id, c.name, val, `${pct}%`]
    }),
  }), [])

  return (
    <section id="overview" className="section">
      <div className="container">

        {/* ── Hero ───────────────────────────────────────────────── */}
        <div className="overview-hero animate-in">
          <h1>
            Customer{' '}
            <span className="gradient-text">Segmentation</span>
            <br />Intelligence Platform
          </h1>
          <p>
            Machine-learning driven customer clustering, basket analysis,
            and promotion optimisation — from raw retail data to actionable insights.
          </p>

          {/* Tech pills */}
          <div className="hero-pills">
            {[
              { label: 'Python / Scikit-learn', dot: '#7c3aed' },
              { label: 'Hierarchical Clustering', dot: '#2dd4bf' },
              { label: 'Apriori / mlxtend',     dot: '#f59e0b' },
              { label: 'RobustScaler scaling',  dot: '#3b82f6' },
              { label: 'Silhouette Analysis',    dot: '#f43f5e' },
            ].map(p => (
              <div key={p.label} className="hero-pill">
                <span className="hero-pill-dot" style={{ background: p.dot }} />
                {p.label}
              </div>
            ))}
          </div>
        </div>

        {/* ── KPI Cards ──────────────────────────────────────────── */}
        <div className="overview-kpis" style={{ marginBottom: '2rem' }}>
          <div className="grid-4" style={{ gridTemplateColumns: 'repeat(5, 1fr)' }}>
            {kpiData.map((kpi, i) => (
              <div key={kpi.id} className="animate-in" style={{ animationDelay: `${i * 0.05}s` }}>
                <KPICard {...kpi} />
              </div>
            ))}
          </div>
        </div>

        <div className="divider" />

        {/* ── Overview insight row ───────────────────────────────── */}
        <div className="overview-insight">

          {/* Left: written summary */}
          <div className="insight-text card animate-in delay-1">
            <SectionHeader
              badge="📋 Executive Summary"
              title="What we "
              highlight="discovered"
              subtitle=""
            />
            <p>
              Applying Hierarchical Clustering (Ward linkage, k=7, RobustScaler) to the customer database of <strong style={{ color: 'var(--teal)' }}>32,571</strong> customers revealed seven distinct behavioral segments with a silhouette score of <strong style={{ color: 'var(--teal)' }}>0.132</strong> — balancing segment cohesion and model complexity. Features were scaled using RobustScaler to minimize the impact of purchase frequency and lifetime value outliers.
            </p>
            <p>
              Basket analysis using the Apriori algorithm was subsequently run for each cluster separately, surfacing strong product affinities (with lift scores reaching up to <strong style={{ color: 'var(--teal)' }}>9.15×</strong>) that can directly inform personalized promotion bundles and discount strategies.
            </p>

            <ul className="insight-list" style={{ marginTop: '1.25rem' }}>
              {[
                '35.6% of customers are Loyal Core Spenders — the largest segment and primary revenue drivers',
                '20.4% are Vegans — healthy lifestyle focus, buying vegetables and organic produce (Cupão: lima5)',
                '17.4% are Bargain Hunters — promo-driven — higher complaints & promotion focus',
                '9.6% are Karens — critical segment with the highest rate of customer complaints and churn risk',
                '6.7% are Tech Enthusiasts & 3.8% are Gamers — evening shoppers buying electronics and entertainment',
                '6.5% are Big Families — high transaction variety and largest dependants count',
                'Airpods + Iphone 10 → Energy Drink + Bluetooth Headphones: highest lift rule at 9.15×',
              ].map(item => (
                <li key={item}>
                  <span className="insight-check">✓</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Right: cluster distribution donut */}
          <div className="animate-in delay-2">
            <InteractivePlot
              title="Customer Segment Distribution"
              description="Share of customers in each Hierarchical cluster (k=7, RobustScaler, Ward linkage). The largest segment is Loyal Core Spenders (35.6%), while the smallest is Gamers (3.8%)."
              data={[donutTrace]}
              layout={donutLayout}
              csvData={donutCsv}
              height={360}
            />
          </div>
        </div>

      </div>
    </section>
  )
}

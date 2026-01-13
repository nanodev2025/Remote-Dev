const LINKS = {
  github: 'https://github.com/nanodev2025/Remote-Dev',
  telegramBot: 'https://t.me/YourBotUsername', // TODO: remplace par ton bot
  twitter: 'https://twitter.com/yourhandle', // placeholder
}

const FEATURES = [
  {
    title: '1. Envoyez votre instruction',
    desc: 'Depuis Telegram, décrivez ce que vous voulez changer en langage naturel.',
    icon: '/icon-send.png',
    alt: "Icône d'envoi de message (placeholder PNG).",
  },
  {
    title: '2. Le bot modifie le code',
    desc: "L'IA analyse et applique les modifications de fichiers (create/modify/delete).",
    icon: '/icon-code.png',
    alt: 'Icône de code < /> (placeholder PNG).',
  },
  {
    title: '3. Preview du diff',
    desc: 'Vous recevez immédiatement le diff des changements. Validez ou annulez avec /reset.',
    icon: '/icon-preview.png',
    alt: 'Icône de preview (placeholder PNG).',
  },
  {
    title: '4. Déployez sur commande',
    desc: 'Utilisez /deploy pour commit + push vers GH. Lien vers le commit inclus.',
    icon: '/icon-github.png',
    alt: 'Icône GitHub stylisée (placeholder PNG).',
  },
]

const BENEFITS = [
  {
    title: 'Productivité mobile',
    desc: 'Une idée dans le métro ? Une correction sur le canapé ? Vous shippez quand vous voulez.',
    icon: 'rocket',
  },
  {
    title: 'Intégration IA',
    desc: 'Des instructions en langage naturel qui se transforment en modifications concrètes.',
    icon: 'lightbulb',
  },
  {
    title: 'Flexibilité totale',
    desc: 'Travaillez depuis n’importe où. Le workflow s’adapte à votre rythme, pas l’inverse.',
    icon: 'globe',
  },
]

function Badge({ children }) {
  return (
    <span className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs text-slate-700">
      <span className="h-2 w-2 rounded-full bg-sky-500" />
      {children}
    </span>
  )
}

function PrimaryButton({ href, children }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      className="group inline-flex items-center justify-center gap-2 rounded-xl bg-sky-500 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-sky-600 focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:ring-offset-2 focus:ring-offset-white"
    >
      {children}
      <span className="transition group-hover:translate-x-0.5">→</span>
    </a>
  )
}

function SecondaryButton({ href, children }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-400/50 focus:ring-offset-2 focus:ring-offset-white"
    >
      {children}
    </a>
  )
}

function GithubBadge({ href }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noreferrer"
      className="group inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 transition hover:bg-slate-50"
      aria-label="Ouvrir le repository GitHub"
      title="GitHub"
    >
      <span className="grid h-5 w-5 place-items-center rounded-full bg-slate-900/5 ring-1 ring-slate-200">
        {/* Icône simple (placeholder) */}
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M12 2c5.52 0 10 4.62 10 10.32 0 4.56-2.87 8.43-6.84 9.8-.5.1-.68-.22-.68-.48v-1.7c0-.58-.19-.96-.4-1.15 1.32-.15 2.7-.68 2.7-3.09 0-.69-.23-1.25-.62-1.69.06-.16.27-.83-.06-1.73 0 0-.5-.17-1.64.65a5.5 5.5 0 0 0-3 0c-1.13-.82-1.64-.65-1.64-.65-.33.9-.12 1.57-.06 1.73-.38.44-.62 1-.62 1.69 0 2.4 1.37 2.94 2.68 3.09-.17.16-.33.43-.38.83-.34.16-1.2.46-1.73-.56 0 0-.32-.6-.93-.64 0 0-.6-.01-.04.38 0 0 .4.2.67.97 0 0 .36 1.16 2.01.78v1.3c0 .26-.18.58-.68.48C4.87 20.75 2 16.88 2 12.32 2 6.62 6.48 2 12 2Z"
            fill="currentColor"
            opacity="0.9"
          />
        </svg>
      </span>
      <span>GitHub</span>
      <span className="text-slate-400 transition group-hover:text-slate-600">↗</span>
    </a>
  )
}

function SectionHeading({ kicker, title, desc }) {
  return (
    <div className="mx-auto max-w-2xl text-center">
      {kicker ? (
        <p className="text-xs font-semibold uppercase tracking-widest text-sky-600">
          {kicker}
        </p>
      ) : null}
      <h2 className="mt-3 text-balance text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
        {title}
      </h2>
      {desc ? (
        <p className="mt-4 text-pretty text-base leading-relaxed text-slate-600">
          {desc}
        </p>
      ) : null}
    </div>
  )
}

function Card({ children }) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-slate-200 bg-white p-8 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
      {/* petit “shimmer” discret au survol */}
      <div className="pointer-events-none absolute inset-0 opacity-0 transition group-hover:opacity-100">
        <div className="absolute -left-1/2 top-0 h-full w-1/2 rotate-12 bg-gradient-to-r from-transparent via-sky-100/30 to-transparent animate-shimmer" />
      </div>
      {children}
    </div>
  )
}

function BenefitIcon({ type }) {
  const icons = {
    rocket: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* Fusée - Productivité mobile */}
        <path
          d="M12 2L9 6.5L12 5.8L15 6.5L12 2Z"
          fill="currentColor"
          className="text-sky-500"
        />
        <rect x="10.5" y="5.8" width="3" height="8" rx="1.5" fill="currentColor" className="text-sky-400" />
        <path
          d="M9 13.8L10.5 16L12 13.8L13.5 16L15 13.8"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          className="text-sky-600"
          fill="none"
        />
        <circle cx="12" cy="9" r="1" fill="currentColor" className="text-white" />
      </svg>
    ),
    lightbulb: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* Ampoule - Intégration IA */}
        <path
          d="M12 2C9.24 2 7 4.24 7 7C7 8.76 7.95 10.25 9.4 11H14.6C16.05 10.25 17 8.76 17 7C17 4.24 14.76 2 12 2Z"
          fill="currentColor"
          className="text-amber-500"
        />
        <path
          d="M10 11V14C10 15.1 10.9 16 12 16C13.1 16 14 15.1 14 14V11H10Z"
          fill="currentColor"
          className="text-amber-400"
        />
        <rect x="11.5" y="16" width="1" height="2" fill="currentColor" className="text-slate-700" />
        <rect x="10" y="18" width="4" height="1" rx="0.5" fill="currentColor" className="text-slate-700" />
        <path
          d="M12 5V7"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          className="text-amber-600"
          fill="none"
        />
      </svg>
    ),
    globe: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* Globe - Flexibilité totale */}
        <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="1.5" className="text-blue-500" fill="none" />
        <ellipse cx="12" cy="12" rx="9" ry="4" fill="currentColor" className="text-blue-100" />
        <path
          d="M3 12C3 8.5 5.5 6 8.5 5M21 12C21 8.5 18.5 6 15.5 5"
          stroke="currentColor"
          strokeWidth="1.5"
          className="text-blue-400"
          fill="none"
        />
        <path
          d="M12 3C12 7 12 11 12 15C12 17 12 19 12 21"
          stroke="currentColor"
          strokeWidth="1.5"
          className="text-blue-400"
          fill="none"
        />
        <circle cx="12" cy="12" r="1.5" fill="currentColor" className="text-blue-600" />
      </svg>
    ),
  }
  
  return <div className="text-sky-600">{icons[type] || icons.rocket}</div>
}

export default function App() {
  return (
    <div className="min-h-screen bg-white">
      {/* Background */}
      <div className="pointer-events-none fixed inset-0 -z-10 bg-white">
        <div className="absolute inset-0 bg-grid opacity-20" />
        <div className="absolute left-1/2 top-[-220px] h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-sky-50 blur-3xl opacity-60" />
        <div className="absolute right-[-180px] top-[120px] h-[520px] w-[520px] rounded-full bg-blue-50 blur-3xl opacity-60" />
      </div>

      {/* Header */}
      <header className="relative mx-auto max-w-6xl px-4 py-6 sm:px-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-2xl bg-sky-50 ring-1 ring-slate-200">
              <span className="text-lg font-black tracking-tight text-sky-600">RD</span>
            </div>
            <div className="leading-tight">
              <p className="text-sm font-semibold text-slate-900">Remote Dev</p>
              <p className="text-xs text-slate-500">Dév remote • Telegram • Git</p>
            </div>
          </div>
          <nav className="hidden items-center gap-6 text-sm text-slate-600 sm:flex">
            <a className="hover:text-slate-900" href="#how">
              Comment ça marche
            </a>
            <a className="hover:text-slate-900" href="#benefits">
              Avantages
            </a>
          </nav>
          <div className="flex items-center gap-3">
            <GithubBadge href={LINKS.github} />
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="relative mx-auto max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-16">
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <div>
            <Badge>Votre environnement de développement dans la poche</Badge>
            <h1 className="mt-5 text-balance text-4xl font-semibold tracking-tight text-slate-900 sm:text-5xl">
              Développez depuis n’importe où avec{' '}
              <span className="text-sky-600">Remote Dev</span>.
            </h1>
            <p className="mt-5 max-w-xl text-pretty text-lg leading-relaxed text-slate-600">
              Envoyez une instruction sur Telegram. Le bot applique les changements via IA, vous montre le diff, 
              puis vous déployez sur commande avec /deploy vers GH.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center">
              <PrimaryButton href={LINKS.github}>Commencer maintenant</PrimaryButton>
            </div>

            <p className="mt-4 text-xs text-slate-500">
              Slogan : <span className="text-slate-700">"Message. Patch. Commit. Repeat."</span>
            </p>
          </div>

          <div className="relative">
            <div className="group relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              {/* Image hero */}
              <div className="relative overflow-hidden rounded-2xl bg-slate-50 ring-1 ring-slate-200">
                <img
                  src="/illu-hero.jpg"
                  alt="Illustration flat design d'un développeur sur un nuage de code, avec un téléphone (Telegram) et un laptop (Cursor/VS Code)."
                  className="h-[320px] w-full object-cover opacity-95 transition duration-500 group-hover:scale-[1.02]"
                  loading="eager"
                  fetchPriority="high"
                  decoding="async"
                />
                <div className="pointer-events-none absolute inset-0 bg-gradient-to-tr from-white/40 via-transparent to-transparent" />
              </div>

              {/* mini “chips” */}
              <div className="mt-5 flex flex-wrap gap-2">
                {['Telegram‑first', 'GitHub‑ready', 'IA‑assisté', 'Remote‑friendly'].map((t) => (
                  <span
                    key={t}
                    className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs text-slate-700"
                  >
                    {t}
                  </span>
                ))}
              </div>
            </div>

            <div className="pointer-events-none absolute -bottom-8 -left-8 hidden h-28 w-28 rounded-3xl bg-sky-50 blur-xl opacity-40 lg:block" />
            <div className="pointer-events-none absolute -top-10 -right-10 hidden h-28 w-28 rounded-3xl bg-blue-50 blur-xl opacity-40 lg:block" />
          </div>
        </div>

        {/* How it works */}
        <section id="how" className="relative mt-20">
          <SectionHeading
            kicker="Comment ça marche"
            title="Un workflow en 4 étapes — sans friction"
            desc="De l'instruction au déploiement : une boucle courte, claire, et contrôlée."
          />

          <div className="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {FEATURES.map((f) => (
              <div key={f.title} className="group">
                <Card>
                  <div className="flex min-h-[120px] flex-col">
                    <h3 className="text-base font-semibold text-slate-900">{f.title}</h3>
                    <p className="mt-3 text-sm leading-relaxed text-slate-600 break-words">{f.desc}</p>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        </section>

        {/* Benefits */}
        <section id="benefits" className="relative mt-20">
          <SectionHeading
            kicker="Pourquoi c’est génial"
            title="Le dev devient mobile, pas fragile"
            desc="Pensé pour les petites itérations, les corrections rapides et le momentum."
          />

          <div className="mt-10 grid gap-4 lg:grid-cols-3">
            {BENEFITS.map((b) => (
              <div key={b.title} className="group">
                <Card>
                  <div className="flex items-start gap-4">
                    <div className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-slate-50 ring-1 ring-slate-200">
                      <BenefitIcon type={b.icon} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-sm font-semibold text-slate-900">{b.title}</h3>
                      <p className="mt-2 text-sm leading-relaxed text-slate-600 break-words">{b.desc}</p>
                    </div>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        </section>

        {/* Final CTA */}
        <section className="relative mt-20">
          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-br from-sky-50 via-white to-blue-50 p-8 shadow-sm">
            <div className="pointer-events-none absolute inset-0">
              <div className="absolute -left-24 top-10 h-60 w-60 rounded-full bg-sky-50 blur-3xl opacity-50" />
              <div className="absolute -right-24 bottom-10 h-60 w-60 rounded-full bg-blue-50 blur-3xl opacity-50" />
            </div>

            <div className="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <h2 className="text-balance text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">
                  Prêt à transformer votre workflow de développement ?
                </h2>
                <p className="mt-3 max-w-2xl text-sm leading-relaxed text-slate-600">
                  Essayez Remote Dev, et gardez votre élan — même loin de votre machine.
                </p>
              </div>
              <div className="flex flex-col gap-3 sm:flex-row">
                <PrimaryButton href={LINKS.github}>GitHub</PrimaryButton>
              </div>
            </div>

            <div className="relative mt-8 flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 pt-6 text-xs text-slate-500">
              <p>© {new Date().getFullYear()} Remote Dev — Tous droits réservés.</p>
              <div className="flex items-center gap-4">
                <a className="hover:text-slate-700" href={LINKS.github} target="_blank" rel="noreferrer">
                  GitHub
                </a>
                <a
                  className="hover:text-slate-700"
                  href={LINKS.twitter}
                  target="_blank"
                  rel="noreferrer"
                >
                  Twitter
                </a>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

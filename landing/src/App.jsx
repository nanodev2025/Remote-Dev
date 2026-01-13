const LINKS = {
  github: 'https://github.com/username/repo', // TODO: remplace par ton repo
  telegramBot: 'https://t.me/YourBotUsername', // TODO: remplace par ton bot
  twitter: 'https://twitter.com/yourhandle', // placeholder
}

const FEATURES = [
  {
    title: '1. Envoyez votre instruction',
    desc: 'Depuis Telegram, décrivez ce que vous voulez changer. Simple, direct, rapide.',
    icon: '/icon-send.png',
    alt: 'Icône d’envoi de message (placeholder PNG).',
  },
  {
    title: '2. Le bot modifie le code',
    desc: 'Analyse + patch de fichiers. Le bot applique des modifications cohérentes.',
    icon: '/icon-code.png',
    alt: 'Icône de code < /> (placeholder PNG).',
  },
  {
    title: '3. Preview instantanée',
    desc: 'Visualisez le résultat rapidement. Ajustez votre demande si nécessaire.',
    icon: '/icon-preview.png',
    alt: 'Icône de preview (placeholder PNG).',
  },
  {
    title: '4. Push automatique sur GitHub',
    desc: 'Commit + push : vos changements sont versionnés, traçables, partageables.',
    icon: '/icon-github.png',
    alt: 'Icône GitHub stylisée (placeholder PNG).',
  },
]

const BENEFITS = [
  {
    title: 'Productivité mobile',
    desc: 'Une idée dans le métro ? Une correction sur le canapé ? Vous shippez quand vous voulez.',
    icon: '/icon-productivity.png',
    alt: 'Icône productivité (fusée/horloge) (placeholder PNG).',
  },
  {
    title: 'Intégration IA',
    desc: 'Des instructions en langage naturel qui se transforment en modifications concrètes.',
    icon: '/icon-ai.png',
    alt: 'Icône IA (ampoule/cerveau) (placeholder PNG).',
  },
  {
    title: 'Flexibilité totale',
    desc: 'Travaillez depuis n’importe où. Le workflow s’adapte à votre rythme, pas l’inverse.',
    icon: '/icon-flexibility.png',
    alt: 'Icône flexibilité (multi-lieux) (placeholder PNG).',
  },
]

const TESTIMONIALS = [
  {
    quote:
      '“J’ai corrigé un bug de prod depuis mon téléphone, avant même d’avoir posé mon café.”',
    name: 'Développeur·se nomade',
    role: 'Full‑stack',
  },
  {
    quote:
      '“Un workflow ultra simple : message → patch → commit. C’est addictif (dans le bon sens).”',
    name: 'Team Lead',
    role: 'Engineering',
  },
  {
    quote:
      '“Parfait pour les petites itérations. Je garde l’élan, même loin du laptop.”',
    name: 'Maker',
    role: 'Indie',
  },
]

function Badge({ children }) {
  return (
    <span className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-200">
      <span className="h-2 w-2 rounded-full bg-sky-400" />
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
      className="group inline-flex items-center justify-center gap-2 rounded-xl bg-sky-400 px-5 py-3 text-sm font-semibold text-slate-950 shadow-soft transition hover:bg-sky-300 focus:outline-none focus:ring-2 focus:ring-sky-300/60 focus:ring-offset-2 focus:ring-offset-slate-950"
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
      className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/12 bg-white/5 px-5 py-3 text-sm font-semibold text-slate-100 transition hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/20 focus:ring-offset-2 focus:ring-offset-slate-950"
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
      className="group inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-semibold text-slate-200 transition hover:bg-white/10"
      aria-label="Ouvrir le repository GitHub"
      title="GitHub"
    >
      <span className="grid h-5 w-5 place-items-center rounded-full bg-slate-900/60 ring-1 ring-white/10">
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
      <span className="text-slate-400 transition group-hover:text-slate-200">↗</span>
    </a>
  )
}

function SectionHeading({ kicker, title, desc }) {
  return (
    <div className="mx-auto max-w-2xl text-center">
      {kicker ? (
        <p className="text-xs font-semibold uppercase tracking-widest text-sky-300/90">
          {kicker}
        </p>
      ) : null}
      <h2 className="mt-3 text-balance text-3xl font-semibold tracking-tight text-slate-50 sm:text-4xl">
        {title}
      </h2>
      {desc ? (
        <p className="mt-4 text-pretty text-base leading-relaxed text-slate-300">
          {desc}
        </p>
      ) : null}
    </div>
  )
}

function Card({ children }) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-6 shadow-soft transition hover:-translate-y-0.5 hover:bg-white/7">
      {/* petit “shimmer” discret au survol */}
      <div className="pointer-events-none absolute inset-0 opacity-0 transition group-hover:opacity-100">
        <div className="absolute -left-1/2 top-0 h-full w-1/2 rotate-12 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer" />
      </div>
      {children}
    </div>
  )
}

export default function App() {
  return (
    <div className="min-h-screen">
      {/* Background */}
      <div className="pointer-events-none fixed inset-0 -z-10 bg-slate-950">
        <div className="absolute inset-0 bg-grid opacity-40" />
        <div className="absolute left-1/2 top-[-220px] h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-sky-500/15 blur-3xl" />
        <div className="absolute right-[-180px] top-[120px] h-[520px] w-[520px] rounded-full bg-violet-500/15 blur-3xl" />
      </div>

      {/* Header */}
      <header className="mx-auto max-w-6xl px-4 py-6 sm:px-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-2xl bg-white/5 ring-1 ring-white/10">
              <span className="text-lg font-black tracking-tight text-sky-300">CRD</span>
            </div>
            <div className="leading-tight">
              <p className="text-sm font-semibold text-slate-100">Cursor Remote Dev</p>
              <p className="text-xs text-slate-400">Dév remote • Telegram • Git</p>
            </div>
          </div>
          <nav className="hidden items-center gap-6 text-sm text-slate-300 sm:flex">
            <a className="hover:text-slate-50" href="#how">
              Comment ça marche
            </a>
            <a className="hover:text-slate-50" href="#benefits">
              Avantages
            </a>
            <a className="hover:text-slate-50" href="#testimonials">
              Témoignages
            </a>
          </nav>
          <div className="flex items-center gap-3">
            <GithubBadge href={LINKS.github} />
            <SecondaryButton href={LINKS.telegramBot}>Ouvrir Telegram</SecondaryButton>
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="mx-auto max-w-6xl px-4 pb-20 pt-10 sm:px-6 sm:pt-16">
        <div className="grid items-center gap-10 lg:grid-cols-2">
          <div>
            <Badge>Votre environnement de développement dans la poche</Badge>
            <h1 className="mt-5 text-balance text-4xl font-semibold tracking-tight text-slate-50 sm:text-5xl">
              Développez depuis n’importe où avec{' '}
              <span className="text-sky-300">Cursor Remote Dev</span>.
            </h1>
            <p className="mt-5 max-w-xl text-pretty text-lg leading-relaxed text-slate-300">
              Envoyez une instruction sur Telegram. Le bot applique les changements dans votre
              repo, vous renvoie un diff clair, puis pousse sur GitHub — sans casser votre flow.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center">
              <PrimaryButton href={LINKS.github}>Commencer maintenant</PrimaryButton>
              <SecondaryButton href={LINKS.telegramBot}>Essayer le bot</SecondaryButton>
            </div>

            <p className="mt-4 text-xs text-slate-400">
              Slogan : <span className="text-slate-200">“Message. Patch. Commit. Repeat.”</span>
            </p>

            <div className="mt-8 grid grid-cols-3 gap-3">
              {[
                { k: 'Flat', v: 'Design minimal' },
                { k: 'Smooth', v: 'Micro‑interactions' },
                { k: 'Secure', v: 'User ID lock' },
              ].map((item) => (
                <div
                  key={item.k}
                  className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3"
                >
                  <p className="text-xs font-semibold text-slate-100">{item.k}</p>
                  <p className="mt-1 text-xs text-slate-400">{item.v}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="relative">
            <div className="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-6 shadow-soft">
              {/* Placeholder image */}
              <div className="relative overflow-hidden rounded-2xl bg-slate-900/60 ring-1 ring-white/10">
                <img
                  src="/image-hero.png"
                  alt="Illustration flat design d’un développeur sur un nuage de code, avec un téléphone (Telegram) et un laptop (Cursor/VS Code). Placeholder PNG."
                  className="h-[320px] w-full object-cover opacity-90 transition duration-500 group-hover:scale-[1.02]"
                />
                {/* commentaire: remplace image-hero.png par une vraie illustration */}
                <div className="pointer-events-none absolute inset-0 bg-gradient-to-tr from-slate-950/40 via-transparent to-transparent" />
              </div>

              {/* mini “chips” */}
              <div className="mt-5 flex flex-wrap gap-2">
                {['Telegram‑first', 'GitHub‑ready', 'IA‑assisté', 'Remote‑friendly'].map((t) => (
                  <span
                    key={t}
                    className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-200"
                  >
                    {t}
                  </span>
                ))}
              </div>
            </div>

            <div className="pointer-events-none absolute -bottom-8 -left-8 hidden h-28 w-28 rounded-3xl bg-sky-400/15 blur-xl lg:block" />
            <div className="pointer-events-none absolute -top-10 -right-10 hidden h-28 w-28 rounded-3xl bg-violet-400/15 blur-xl lg:block" />

            {/* petit élément flottant */}
            <div className="absolute -left-4 top-10 hidden animate-floaty rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-xs text-slate-200 shadow-soft lg:block">
              <span className="font-semibold text-sky-300">Preview</span> en 1 message
            </div>
          </div>
        </div>

        {/* How it works */}
        <section id="how" className="mt-20">
          <SectionHeading
            kicker="Comment ça marche"
            title="Un workflow en 4 étapes — sans friction"
            desc="De l’idée au commit : une boucle courte, claire, et agréable à utiliser."
          />

          <div className="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {FEATURES.map((f) => (
              <div key={f.title} className="group">
                <Card>
                  <div className="flex items-start gap-4">
                    <div className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-slate-900/60 ring-1 ring-white/10">
                      <img
                        src={f.icon}
                        alt={f.alt}
                        className="h-6 w-6 opacity-90"
                      />
                      {/* commentaire: remplace par une vraie icône PNG */}
                    </div>
                    <div>
                      <h3 className="text-sm font-semibold text-slate-50">{f.title}</h3>
                      <p className="mt-2 text-sm leading-relaxed text-slate-300">{f.desc}</p>
                    </div>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        </section>

        {/* Benefits */}
        <section id="benefits" className="mt-20">
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
                    <div className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-slate-900/60 ring-1 ring-white/10">
                      <img src={b.icon} alt={b.alt} className="h-6 w-6 opacity-90" />
                      {/* commentaire: remplace par une vraie icône PNG */}
                    </div>
                    <div>
                      <h3 className="text-sm font-semibold text-slate-50">{b.title}</h3>
                      <p className="mt-2 text-sm leading-relaxed text-slate-300">{b.desc}</p>
                    </div>
                  </div>
                </Card>
              </div>
            ))}
          </div>

          <div className="mt-10 rounded-3xl border border-white/10 bg-white/5 p-6 shadow-soft sm:p-8">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm font-semibold text-slate-50">Proposition de valeur unique</p>
                <p className="mt-2 text-sm text-slate-300">
                  Un bot Telegram qui transforme des intentions en modifications de code traçables.
                </p>
              </div>
              <div className="flex gap-3">
                <SecondaryButton href={LINKS.github}>Voir le repo</SecondaryButton>
                <PrimaryButton href={LINKS.telegramBot}>Lancer sur Telegram</PrimaryButton>
              </div>
            </div>
          </div>
        </section>

        {/* Testimonials */}
        <section id="testimonials" className="mt-20">
          <SectionHeading
            kicker="Témoignages"
            title="Des retours qui donnent envie"
            desc="Placeholders pour l’esthétique — remplace par de vrais avis quand tu en as."
          />

          <div className="mt-10 grid gap-4 lg:grid-cols-3">
            {TESTIMONIALS.map((t) => (
              <div key={t.name} className="group">
                <Card>
                  <p className="text-sm leading-relaxed text-slate-200">{t.quote}</p>
                  <div className="mt-5 flex items-center gap-3">
                    <div className="grid h-10 w-10 place-items-center rounded-2xl bg-slate-900/60 ring-1 ring-white/10">
                      <span className="text-xs font-bold text-sky-300">
                        {t.name.split(' ')[0]?.slice(0, 2).toUpperCase()}
                      </span>
                    </div>
                    <div className="leading-tight">
                      <p className="text-sm font-semibold text-slate-50">{t.name}</p>
                      <p className="text-xs text-slate-400">{t.role}</p>
                    </div>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        </section>

        {/* Final CTA */}
        <section className="mt-20">
          <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-sky-400/10 via-white/5 to-violet-400/10 p-8 shadow-soft">
            <div className="pointer-events-none absolute inset-0">
              <div className="absolute -left-24 top-10 h-60 w-60 rounded-full bg-sky-400/15 blur-3xl" />
              <div className="absolute -right-24 bottom-10 h-60 w-60 rounded-full bg-violet-400/15 blur-3xl" />
            </div>

            <div className="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <h2 className="text-balance text-2xl font-semibold tracking-tight text-slate-50 sm:text-3xl">
                  Prêt à transformer votre workflow de développement ?
                </h2>
                <p className="mt-3 max-w-2xl text-sm leading-relaxed text-slate-300">
                  Essayez Cursor Remote Dev, et gardez votre élan — même loin de votre machine.
                </p>
              </div>
              <div className="flex flex-col gap-3 sm:flex-row">
                <PrimaryButton href={LINKS.telegramBot}>Essayer sur Telegram</PrimaryButton>
                <SecondaryButton href={LINKS.github}>Voir le code</SecondaryButton>
              </div>
            </div>

            <div className="relative mt-8 flex flex-wrap items-center justify-between gap-3 border-t border-white/10 pt-6 text-xs text-slate-400">
              <p>© {new Date().getFullYear()} Cursor Remote Dev — Tous droits réservés.</p>
              <div className="flex items-center gap-4">
                <a className="hover:text-slate-200" href={LINKS.github} target="_blank" rel="noreferrer">
                  GitHub
                </a>
                <a
                  className="hover:text-slate-200"
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


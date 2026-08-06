type AppHeaderProps = {
  title?: string;
};

export function AppHeader({ title = "EagleEye v2" }: AppHeaderProps) {
  return (
    <header className="flex items-center justify-between border-b px-6 py-4">
      <div>
        <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">Workspace</p>
        <h1 className="text-lg font-medium">{title}</h1>
      </div>
    </header>
  );
}


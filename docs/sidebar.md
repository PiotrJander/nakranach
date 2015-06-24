# Menu na pasku bocznym

```
app.main.sidebar_utils:
    sidebar_mixin_factory
    SidebarContextMixin
```

Każdy widok, którego szablon dziedziczy z `base_framed.html`, wymaga w kontekście
szablonu `'sidebar_menu': SidebarMenu instance`.

W przypadku widoków CBVs można to osiągnąć w prosty sposób przez użycie w klasie
widoku specjalnego mixinu generenowanego przez `sidebar_mixin_factory`.

W przypadku bazowych CBVs (`View, TemplateView`) należy użyć mixinu
`SidebarContextMixin`, który jest generowany w ten sposób:

    SidebarContextMixin = sidebar_mixin_factory(ContextMixin)

Przykład użycia `SidebarContextMixin`:

    class MyView(SidebarContextMixin, TemplateView): pass

W przypadku rodzajowych GCBVs należy samodzielnie wygenerować mixin.

Rozważmy widok CBV, który dziedziczy z `DetailView`. `DetailView` używa mixinu
`SingleObjectMixin`, więc aby zachować funkcjonalność `SingleObjectMixin`,
nasz mixin należy wygenerować z `SidebarContextMixin`:

    SingleObjectSidebarContextMixin = sidebar_mixin_factory(SingleObjectMixin)

    class MyView(SingleObjectSidebarContextMixin, DeatilView): pass

Każdy mixin wygenerowany przez `sidebar_mixin_factory` nadpisuje dwie metody:
`get_context_data` i `get`.


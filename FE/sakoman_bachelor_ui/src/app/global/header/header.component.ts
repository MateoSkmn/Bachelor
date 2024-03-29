import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  @Input()
  index: number = -1;

  links = [
    { label: 'Datensätze', url: '/data' },
    { label: 'Modelle', url: '/model' },
    { label: 'LIME', url: '/lime' }
  ];
}

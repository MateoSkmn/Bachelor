import { Component } from '@angular/core';
import { HeaderComponent } from '../../global/components/header/header.component';

@Component({
  selector: 'app-page-not-found',
  standalone: true,
  imports: [HeaderComponent],
  templateUrl: './page-not-found.component.html',
  styleUrl: './page-not-found.component.scss'
})
export class PageNotFoundComponent {

}
